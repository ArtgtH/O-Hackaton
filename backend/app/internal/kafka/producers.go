package kafka

import (
	"encoding/json"
	"github.com/IBM/sarama"
	"github.com/sirupsen/logrus"
	"log"
	"webapp/app/config"
	"webapp/app/internal/dto"
)

func SendFile(task dto.TaskInputWithFile) error {
	kafka := config.Config("KAFKA_BROKERS")
	kafkaConfig := sarama.NewConfig()
	kafkaConfig.Producer.RequiredAcks = sarama.WaitForAll
	kafkaConfig.Producer.Retry.Max = 5
	kafkaConfig.Producer.Return.Successes = true

	producer, err := sarama.NewSyncProducer([]string{kafka}, kafkaConfig)
	if err != nil {
		return err
	}
	defer producer.Close()

	message := map[string]interface{}{
		"task_id": task.ID,
		"type":    "file",
		"data":    task.File,
	}

	msgBytes, err := json.Marshal(message)

	logrus.Info(msgBytes)

	if err != nil {
		log.Printf("Failed to marshal message: %v", err)
		return err
	}

	msg := &sarama.ProducerMessage{
		Topic: "ml-input",
		Value: sarama.ByteEncoder(msgBytes),
	}

	_, _, err = producer.SendMessage(msg)

	logrus.Info(msg)

	if err != nil {
		return err
	}
	return nil
}

func SendString(task dto.TaskInputWithString) error {
	kafka := config.Config("KAFKA_BROKERS")
	kafkaConfig := sarama.NewConfig()
	kafkaConfig.Producer.RequiredAcks = sarama.WaitForAll
	kafkaConfig.Producer.Retry.Max = 5
	kafkaConfig.Producer.Return.Successes = true

	producer, err := sarama.NewSyncProducer([]string{kafka}, kafkaConfig)
	if err != nil {
		return err
	}
	defer producer.Close()

	message := map[string]interface{}{
		"task_id": task.ID,
		"type":    "string",
		"data":    task.Data,
	}

	msgBytes, err := json.Marshal(message)
	if err != nil {
		log.Printf("Failed to marshal message: %v", err)
		return err
	}

	msg := &sarama.ProducerMessage{
		Topic: "ml-input",
		Value: sarama.ByteEncoder(msgBytes),
	}

	_, _, err = producer.SendMessage(msg)
	if err != nil {
		return err
	}
	return nil
}
