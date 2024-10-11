package database

import (
	"fmt"
	"log"
	"strconv"
	"webapp/app/config"
	"webapp/app/internal/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func ConnectDB() {
	p := config.Config("DB_PORT")
	port, err := strconv.ParseUint(p, 10, 32)

	if err != nil {
		log.Println("Invalid port number")
	}

	dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", config.Config("DB_HOST"), port, config.Config("DB_USER"), config.Config("DB_PASSWORD"), config.Config("DB_NAME"))
	DB, err = gorm.Open(postgres.Open(dsn))
	if err != nil {
		panic("failed to connect database")
	}

	fmt.Println("Connection Opened to Database")

	err = DB.AutoMigrate(&models.User{})
	if err != nil {
		log.Println("Database migration failed")
	}
	log.Println("Database Migrated")
}
