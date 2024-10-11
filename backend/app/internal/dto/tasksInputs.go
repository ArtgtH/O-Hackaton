package dto

import "github.com/google/uuid"

type TaskInputWithFile struct {
	ID   uuid.UUID `json:"id"`
	File []byte    `json:"file"`
}

type TaskInputWithString struct {
	ID   uuid.UUID `json:"id"`
	Data string    `json:"data"`
}
