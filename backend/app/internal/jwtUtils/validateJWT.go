package jwtUtils

import (
	"github.com/golang-jwt/jwt/v5"
	"gorm.io/gorm"
	"webapp/app/internal/models"
)

func ValidateUserWithJWT(db *gorm.DB, payload jwt.MapClaims) (models.User, error) {
	email := payload["sub"].(string)

	foundUser := models.User{}
	if err := db.Where("email = ?", email).First(&foundUser).Error; err != nil {
		return foundUser, nil
	} else {
		return foundUser, err
	}
}
