package config

import (
	"github.com/sirupsen/logrus"
	"os"

	"github.com/joho/godotenv"
)

func Config(key string) string {
	err := godotenv.Load(".env")
	if err != nil {
		logrus.Info(".env file not found")
	}

	return os.Getenv(key)
}
