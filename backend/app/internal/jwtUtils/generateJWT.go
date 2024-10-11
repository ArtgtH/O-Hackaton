package jwtUtils

import (
	"github.com/golang-jwt/jwt/v5"
	"time"
	"webapp/app/internal/models"
)

func GenerateJWT(user models.User) (string, error) {

	payload := jwt.MapClaims{
		"sub": user.Email,
		"exp": time.Now().Add(time.Hour * 24 * 7).Unix(),
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, payload)

	tokenString, err := token.SignedString(JwtKey)

	if err != nil {
		return "", err
	}
	return tokenString, nil
}
