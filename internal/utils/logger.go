package utils

import (
	"github.com/sirupsen/logrus"
)

var logger *logrus.Logger

func InitLogger(level string, debug bool) {
	logger = logrus.New()

	// Set log level
	switch level {
	case "DEBUG":
		logger.SetLevel(logrus.DebugLevel)
	case "INFO":
		logger.SetLevel(logrus.InfoLevel)
	case "WARN":
		logger.SetLevel(logrus.WarnLevel)
	case "ERROR":
		logger.SetLevel(logrus.ErrorLevel)
	default:
		logger.SetLevel(logrus.InfoLevel)
	}

	// Set formatter
	if debug {
		logger.SetFormatter(&logrus.TextFormatter{
			FullTimestamp: true,
		})
	} else {
		logger.SetFormatter(&logrus.JSONFormatter{})
	}
}

func GetLogger() *logrus.Logger {
	if logger == nil {
		InitLogger("INFO", false)
	}
	return logger
}
