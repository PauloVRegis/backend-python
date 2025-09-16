package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"backend-python/internal/auth"
	"backend-python/internal/config"
	"backend-python/internal/database"
	"backend-python/internal/handlers"
	"backend-python/internal/metrics"
	"backend-python/internal/middleware"
	"backend-python/internal/utils"
	_ "backend-python/docs" // Import generated docs

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

// @title SmartForce API
// @version 1.0
// @description A comprehensive workout training application with user management and exercise tracking
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.url http://www.swagger.io/support
// @contact.email support@swagger.io

// @license.name MIT
// @license.url https://opensource.org/licenses/MIT

// @host localhost:8000
// @BasePath /api/v1

// @securityDefinitions.apikey ApiKeyAuth
// @in header
// @name Authorization
// @description Type "Bearer" followed by a space and JWT token.

func main() {
	// Load configuration
	cfg := config.LoadConfig()

	// Initialize logger
	utils.InitLogger(cfg.LogLevel, cfg.Debug)
	logger := utils.GetLogger()

	// Initialize authentication
	auth.InitAuth(cfg)

	// Initialize database
	if err := database.InitDatabase(cfg); err != nil {
		logger.Fatalf("Failed to initialize database: %v", err)
	}

	// Set Gin mode
	if !cfg.Debug {
		gin.SetMode(gin.ReleaseMode)
	}

	// Create Gin router
	router := gin.New()

	// Add middleware
	router.Use(middleware.LoggingMiddleware())
	router.Use(gin.Recovery())
	router.Use(middleware.RequestIDMiddleware())
	router.Use(middleware.CORSMiddleware(cfg.AllowedOrigins))
	router.Use(metrics.PrometheusMiddleware())

	// Rate limiting
	rateLimiter := middleware.NewRateLimiter(cfg.RateLimitPerMinute)
	router.Use(rateLimiter.Middleware())

	// Health check endpoint
	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "healthy",
			"timestamp": time.Now().UTC(),
			"version":   "1.0.0",
		})
	})

	// Root endpoint with API information
	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"name":        "SmartForce API",
			"version":     "1.0.0",
			"description": "A comprehensive workout training application with user management and exercise tracking",
			"go_version":  "Migrated from Python/FastAPI to Go/Gin",
			"endpoints": gin.H{
				"health":        "/health",
				"metrics":       "/metrics",
				"documentation": "/docs/index.html",
				"swagger_json":  "/docs/swagger.json",
				"swagger_yaml":  "/docs/swagger.yaml",
				"api_base":      "/api/v1",
				"auth": gin.H{
					"login":    "POST /api/v1/auth/login",
					"register": "POST /api/v1/auth/register",
					"me":       "GET /api/v1/auth/me (authenticated)",
				},
				"public": gin.H{
					"exercises":  "GET /api/v1/exercises",
					"professors": "GET /api/v1/professors",
				},
			},
			"documentation": "Interactive API documentation available at /docs/index.html with full Swagger UI",
		})
	})

	// Swagger documentation
	if cfg.Debug {
		router.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
	}

	// Metrics endpoint
	router.GET("/metrics", metrics.Handler())

	// API v1 routes
	v1 := router.Group("/api/v1")

	// Initialize handlers
	authHandler := handlers.NewAuthHandler(cfg)
	userHandler := handlers.NewUserHandler()
	professorHandler := handlers.NewProfessorHandler()
	exerciseHandler := handlers.NewExerciseHandler()
	trainingHandler := handlers.NewTrainingHandler()

	// Public routes (no authentication required)
	public := v1.Group("/")
	{
		// Auth routes
		auth := public.Group("/auth")
		{
			auth.POST("/login", authHandler.Login)
			auth.POST("/register", authHandler.Register)
		}

		// Public exercise routes
		exercises := public.Group("/exercises")
		{
			exercises.GET("", exerciseHandler.GetExercises)
			exercises.GET("/:id", exerciseHandler.GetExercise)
			exercises.GET("/muscle-groups", exerciseHandler.GetMuscleGroups)
		}

		// Public professor routes
		professors := public.Group("/professors")
		{
			professors.GET("", professorHandler.GetProfessors)
			professors.GET("/:id", professorHandler.GetProfessor)
		}
	}

	// Protected routes (authentication required)
	protected := v1.Group("/")
	protected.Use(middleware.AuthMiddleware())
	{
		// Auth protected routes
		auth := protected.Group("/auth")
		{
			auth.POST("/refresh", authHandler.RefreshToken)
			auth.GET("/me", authHandler.GetMe)
		}

		// User routes
		users := protected.Group("/users")
		{
			users.GET("", userHandler.GetUsers)
			users.GET("/:id", userHandler.GetUser)
			users.POST("", userHandler.CreateUser)
			users.PUT("/:id", userHandler.UpdateUser)
			users.DELETE("/:id", userHandler.DeleteUser)
		}

		// Professor management routes (authenticated)
		professors := protected.Group("/professors")
		{
			professors.POST("", professorHandler.CreateProfessor)
			professors.PUT("/:id", professorHandler.UpdateProfessor)
			professors.DELETE("/:id", professorHandler.DeleteProfessor)
		}

		// Exercise management routes (authenticated)
		exercises := protected.Group("/exercises")
		{
			exercises.POST("", exerciseHandler.CreateExercise)
			exercises.PUT("/:id", exerciseHandler.UpdateExercise)
			exercises.DELETE("/:id", exerciseHandler.DeleteExercise)
		}

		// Training routes
		trainings := protected.Group("/trainings")
		{
			trainings.GET("", trainingHandler.GetTrainings)
			trainings.GET("/:id", trainingHandler.GetTraining)
			trainings.POST("", trainingHandler.CreateTraining)
			trainings.PUT("/:id", trainingHandler.UpdateTraining)
			trainings.DELETE("/:id", trainingHandler.DeleteTraining)
			trainings.POST("/:id/exercises", trainingHandler.AddExerciseToTraining)
		}
	}

	// Create HTTP server
	srv := &http.Server{
		Addr:         ":" + cfg.Port,
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Start server in a goroutine
	go func() {
		logger.Infof("Server starting on port %s", cfg.Port)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	logger.Info("Shutting down server...")

	// Graceful shutdown with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Fatalf("Server forced to shutdown: %v", err)
	}

	// Close database connection
	if err := database.CloseDatabase(); err != nil {
		logger.Errorf("Failed to close database: %v", err)
	}

	logger.Info("Server exited")
}
