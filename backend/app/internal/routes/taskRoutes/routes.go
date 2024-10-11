package taskRoutes

import (
	"github.com/gofiber/fiber/v2"
	"webapp/app/internal/handlers/taskHandlers"
)

func SetupTaskRoutes(router fiber.Router) {
	note := router.Group("/tasks")

	note.Post("/file-task/", taskHandlers.CreateTaskWithFile)

	note.Post("/str-task/", taskHandlers.CreateTaskWithStr)
}
