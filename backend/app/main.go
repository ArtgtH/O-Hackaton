package main

import (
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/sirupsen/logrus"
	"os"
	"webapp/app/database"
	"webapp/app/router"
)

func main() {
	webApp := fiber.New()

	staticDir := "./static"

	if err := os.MkdirAll(staticDir, 0755); err != nil {
		fmt.Printf("Error creating static directory: %v\n", err)
		return
	}

	webApp.Use(cors.New())
	webApp.Static("/static", staticDir)

	database.ConnectDB()

	webApp.Use(logger.New(logger.Config{
		Format:     "${time} ${method} ${path} - ${status} - ${latency}\n",
		TimeFormat: "2006-01-02 15:04:05",
	}))

	router.SetupRoutes(webApp)

	webApp.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, World!")
	})

	logrus.Fatal(webApp.Listen(":3000"))
}
