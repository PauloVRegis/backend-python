package database

import (
	"fmt"
	"log"
	"strings"
	"time"

	"backend-python/internal/config"
	"backend-python/internal/models"

	"gorm.io/driver/postgres"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var DB *gorm.DB

func InitDatabase(cfg *config.Config) error {
	var err error
	var dialector gorm.Dialector

	// Configure database based on URL
	if strings.HasPrefix(cfg.DatabaseURL, "postgresql://") || strings.HasPrefix(cfg.DatabaseURL, "postgres://") {
		dialector = postgres.Open(cfg.DatabaseURL)
	} else if strings.HasPrefix(cfg.DatabaseURL, "sqlite://") {
		// Remove sqlite:// prefix for SQLite
		dbPath := strings.TrimPrefix(cfg.DatabaseURL, "sqlite://")
		dialector = sqlite.Open(dbPath)
	} else {
		// Default to SQLite if no prefix
		dialector = sqlite.Open(cfg.DatabaseURL)
	}

	// Configure GORM logger
	var gormLogger logger.Interface
	if cfg.Debug {
		gormLogger = logger.Default.LogMode(logger.Info)
	} else {
		gormLogger = logger.Default.LogMode(logger.Silent)
	}

	// Connect to database
	DB, err = gorm.Open(dialector, &gorm.Config{
		Logger: gormLogger,
		NowFunc: func() time.Time {
			return time.Now().UTC()
		},
	})
	if err != nil {
		return fmt.Errorf("failed to connect to database: %w", err)
	}

	// Get underlying sql.DB to configure connection pool
	sqlDB, err := DB.DB()
	if err != nil {
		return fmt.Errorf("failed to get underlying sql.DB: %w", err)
	}

	// Configure connection pool
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(100)
	sqlDB.SetConnMaxLifetime(time.Hour)

	// Run migrations
	if err := migrate(); err != nil {
		return fmt.Errorf("failed to run migrations: %w", err)
	}

	log.Println("Database connected and migrated successfully")
	return nil
}

func migrate() error {
	return DB.AutoMigrate(
		&models.User{},
		&models.Professor{},
		&models.Exercise{},
		&models.Training{},
		&models.TrainingExercise{},
		&models.TrainingRegistration{},
	)
}

func GetDB() *gorm.DB {
	return DB
}

func CloseDatabase() error {
	sqlDB, err := DB.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}
