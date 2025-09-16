package config

import (
	"os"
	"strconv"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	// Database Configuration
	DatabaseURL string

	// Security
	SecretKey               string
	Algorithm               string
	AccessTokenExpireMinutes int

	// Application Settings
	Debug       bool
	Environment string
	LogLevel    string
	Port        string

	// CORS Settings
	AllowedOrigins []string

	// Rate Limiting
	RateLimitPerMinute int

	// Cache Settings
	RedisURL string

	// Email Settings
	SMTPHost     string
	SMTPPort     int
	SMTPUser     string
	SMTPPassword string
}

func LoadConfig() *Config {
	// Load .env file if it exists
	godotenv.Load()

	return &Config{
		DatabaseURL:              getEnv("DATABASE_URL", "sqlite://./smart_force.db"),
		SecretKey:               getEnv("SECRET_KEY", "your-secret-key-here-make-it-long-and-random"),
		Algorithm:               getEnv("ALGORITHM", "HS256"),
		AccessTokenExpireMinutes: getEnvAsInt("ACCESS_TOKEN_EXPIRE_MINUTES", 30),
		Debug:                   getEnvAsBool("DEBUG", false),
		Environment:             getEnv("ENVIRONMENT", "development"),
		LogLevel:                getEnv("LOG_LEVEL", "INFO"),
		Port:                    getEnv("PORT", "8000"),
		AllowedOrigins: strings.Split(
			getEnv("ALLOWED_ORIGINS", "http://localhost:3000,http://172.25.45.73:8081,exp://172.25.45.73:8081"),
			",",
		),
		RateLimitPerMinute: getEnvAsInt("RATE_LIMIT_PER_MINUTE", 60),
		RedisURL:           getEnv("REDIS_URL", ""),
		SMTPHost:           getEnv("SMTP_HOST", ""),
		SMTPPort:           getEnvAsInt("SMTP_PORT", 587),
		SMTPUser:           getEnv("SMTP_USER", ""),
		SMTPPassword:       getEnv("SMTP_PASSWORD", ""),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvAsInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvAsBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}
