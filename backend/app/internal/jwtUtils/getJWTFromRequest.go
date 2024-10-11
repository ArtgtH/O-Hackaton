package jwtUtils

import (
	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
	"github.com/sirupsen/logrus"
)

func JWTPayloadFromRequest(c *fiber.Ctx) (jwt.MapClaims, bool) {
	jwtToken, ok := c.Context().Value(ContextKeyUser).(*jwt.Token)
	if !ok {
		logrus.WithFields(logrus.Fields{
			"jwt_token_context_value": c.Context().Value(ContextKeyUser),
		}).Error("wrong type of JWT token in context")
		return nil, false
	}

	payload, ok := jwtToken.Claims.(jwt.MapClaims)
	if !ok {
		return nil, false
	}

	return payload, true
}
