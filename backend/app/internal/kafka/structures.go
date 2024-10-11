package kafka

import "github.com/google/uuid"

type (
	FileTaskRes struct {
		ID        uuid.UUID `json:"task_id"`
		Data      []byte    `json:"data"`
		Result    []byte    `json:"result"`
		ResultCsv []byte    `json:"result_csv"`
	}

	StrTaskRes struct {
		ID        uuid.UUID `json:"task_id"`
		Data      []byte    `json:"data"`
		Result    []byte    `json:"result"`
		ResultCsv []byte    `json:"result_csv"`
		Accuracy  []byte    `json:"accuracy"`
	}
)
