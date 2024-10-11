package authRoutes

import (
	"github.com/gofiber/fiber/v2"
	"webapp/app/internal/handlers/authHandlers"
)

func SetupAuthRoutes(router fiber.Router) {
	note := router.Group("")

	note.Post("/login/", authHandlers.Login)

	note.Post("/register/", authHandlers.Register)

	note.Post("/user-check/", authHandlers.CheckUserExists)
}
