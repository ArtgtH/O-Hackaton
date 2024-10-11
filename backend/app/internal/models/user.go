package models

type User struct {
	Email    string `gorm:"primary_key;type:text"`
	Password string `gorm:"type:text;default:'none'"`
}
