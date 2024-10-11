package authHandlers

import (
	"github.com/gofiber/fiber/v2"
	"webapp/app/database"
	"webapp/app/internal/jwtUtils"
	"webapp/app/internal/models"

	"golang.org/x/crypto/bcrypt"
)

func Register(c *fiber.Ctx) error {
	db := database.DB
	signUp := SignUpRequest{}
	if err := c.BodyParser(&signUp); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	foundUser := models.User{}
	if err := db.Where("email = ?", signUp.Email).First(&foundUser).Error; err == nil {
		return c.Status(fiber.StatusConflict).JSON(fiber.Map{"error": "User already exists"})
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(signUp.Password), bcrypt.DefaultCost)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to hash password"})
	}
	newUser := models.User{
		Email:    signUp.Email,
		Password: string(hashedPassword),
	}

	if err = db.Create(&newUser).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to create user"})
	}

	return c.SendStatus(fiber.StatusCreated)
}

func Login(c *fiber.Ctx) error {
	db := database.DB

	signIn := SignInRequest{}
	if err := c.BodyParser(&signIn); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	user := models.User{}
	if err := db.Where("email = ?", signIn.Email).First(&user).Error; err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Invalid email or password"})
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(signIn.Password)); err != nil {
		return c.Status(fiber.StatusUnauthorized).JSON(fiber.Map{"error": "Invalid email or password"})
	}

	token, err := jwtUtils.GenerateJWT(user)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to generate token"})
	}

	return c.JSON(SignInResponse{JWTToken: token})
}

func CheckUserExists(c *fiber.Ctx) error {
	db := database.DB
	user := CheckUserRequest{}

	if err := c.BodyParser(&user); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	targetUser := models.User{}
	if err := db.Where("email = ?", user.Email).First(&targetUser).Error; err != nil {
		return c.Status(fiber.StatusOK).JSON(fiber.Map{"result": false})
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{"result": true})
}
