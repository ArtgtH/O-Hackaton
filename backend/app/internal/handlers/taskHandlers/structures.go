package taskHandlers

import "github.com/google/uuid"

type CreateTaskRequestWithStr struct {
	Data string `json:"data"`
}

type TaskInputWithFile struct {
	ID   uuid.UUID
	File string
}

type TaskInputWithString struct {
	ID   uuid.UUID
	Data string `json:"data"`
}

type FinishedFileTask struct {
	ID     uuid.UUID
	Data   string
	Result string
}
