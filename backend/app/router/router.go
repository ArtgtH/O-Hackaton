package router

import (
	jwtware "github.com/gofiber/contrib/jwt"
	"github.com/gofiber/fiber/v2"
	"webapp/app/internal/jwtUtils"
	"webapp/app/internal/routes/authRoutes"
	"webapp/app/internal/routes/taskRoutes"
)

func SetupRoutes(app *fiber.App) {
	api := app.Group("/api")

	api.Use(jwtware.New(jwtware.Config{
		SigningKey: jwtware.SigningKey{
			Key: jwtUtils.JwtKey,
		},
		ContextKey: jwtUtils.ContextKeyUser,
	}))

	taskRoutes.SetupTaskRoutes(api)
	authRoutes.SetupAuthRoutes(app)
}
