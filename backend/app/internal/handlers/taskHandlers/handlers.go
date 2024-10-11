package taskHandlers

import (
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
	"io/ioutil"
	"path/filepath"
	"webapp/app/database"
	"webapp/app/internal/dto"
	"webapp/app/internal/jwtUtils"
	"webapp/app/internal/kafka"
)

const staticDir = "./static"

func CreateTaskWithFile(c *fiber.Ctx) error {

	jwtPayload, ok := jwtUtils.JWTPayloadFromRequest(c)
	if !ok {
		return c.SendStatus(fiber.StatusUnauthorized)
	}
	db := database.DB
	_, err := jwtUtils.ValidateUserWithJWT(db, jwtPayload)
	if err != nil {
		return c.SendStatus(fiber.StatusUnauthorized)
	}

	file, err := c.FormFile("file")
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	fileBytes, err := file.Open()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	defer fileBytes.Close()

	fileContent, err := ioutil.ReadAll(fileBytes)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	task := dto.TaskInputWithFile{
		ID:   uuid.New(),
		File: fileContent,
	}

	if err = kafka.SendFile(task); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	result, err := kafka.GetFinishedFileTask(task.ID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	filePathJson := filepath.Join(staticDir, fmt.Sprintf("%s.json", result.ID))
	filePathCsv := filepath.Join(staticDir, fmt.Sprintf("%s.csv", result.ID))

	if err = ioutil.WriteFile(filePathJson, result.Result, 0644); err != nil {
		return c.Status(fiber.StatusInternalServerError).SendString("Error saving file")
	}

	if err = ioutil.WriteFile(filePathCsv, result.ResultCsv, 0644); err != nil {
		return c.Status(fiber.StatusInternalServerError).SendString("Error saving file")
	}

	return c.Status(fiber.StatusCreated).JSON(fiber.Map{"result": filePathJson, "result_csv": filePathCsv})
}

func CreateTaskWithStr(c *fiber.Ctx) error {
	jwtPayload, ok := jwtUtils.JWTPayloadFromRequest(c)
	if !ok {
		return c.SendStatus(fiber.StatusUnauthorized)
	}
	db := database.DB
	_, err := jwtUtils.ValidateUserWithJWT(db, jwtPayload)
	if err != nil {
		return c.SendStatus(fiber.StatusUnauthorized)
	}

	taskReq := CreateTaskRequestWithStr{}
	if err = c.BodyParser(&taskReq); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	if taskReq.Data == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "data is required"})
	}

	task := dto.TaskInputWithString{
		ID:   uuid.New(),
		Data: taskReq.Data,
	}

	if err = kafka.SendString(task); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	result, err := kafka.GetFinishedStrTask(task.ID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	jsonFilePath := filepath.Join(staticDir, fmt.Sprint(result.ID, ".json"))

	csvFilePath := filepath.Join(staticDir, fmt.Sprint(result.ID, ".csv"))

	jsonAccFilePath := filepath.Join(staticDir, fmt.Sprint(result.ID, "-accuracy.json"))

	if err = ioutil.WriteFile(csvFilePath, result.ResultCsv, 0644); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	if err = ioutil.WriteFile(jsonFilePath, result.Result, 0644); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	if err = ioutil.WriteFile(jsonAccFilePath, result.Accuracy, 0644); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(fiber.Map{"result": jsonFilePath, "result_csv": csvFilePath, "accuracy": jsonAccFilePath})
}
