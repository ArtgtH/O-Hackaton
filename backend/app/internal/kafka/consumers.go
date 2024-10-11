package kafka

import (
	"encoding/json"
	"github.com/IBM/sarama"
	"github.com/google/uuid"
	"log"
	"webapp/app/config"
)

func GetFinishedFileTask(targetTaskID uuid.UUID) (FileTaskRes, error) {
	kafka := config.Config("KAFKA_BROKERS")

	kafkaConfig := sarama.NewConfig()
	kafkaConfig.Consumer.Return.Errors = true
	kafkaConfig.Version = sarama.V2_6_0_0

	task := FileTaskRes{}

	consumer, err := sarama.NewConsumer([]string{kafka}, kafkaConfig)
	if err != nil {
		return task, err
	}
	defer consumer.Close()

	topic := "finished-file-tasks"
	partitionConsumer, err := consumer.ConsumePartition(topic, 0, sarama.OffsetNewest)
	if err != nil {
		return task, err
	}
	defer partitionConsumer.Close()

	for {
		msg := <-partitionConsumer.Messages()

		task = FileTaskRes{}

		err = json.Unmarshal(msg.Value, &task)
		if err != nil {
			log.Printf("Error unmarshalling message: %s\n", err)
		}

		if task.ID == targetTaskID {
			return task, nil
		}
	}
}

func GetFinishedStrTask(targetTaskID uuid.UUID) (StrTaskRes, error) {
	kafka := config.Config("KAFKA_BROKERS")

	kafkaConfig := sarama.NewConfig()
	kafkaConfig.Consumer.Return.Errors = true
	kafkaConfig.Version = sarama.V2_6_0_0

	task := StrTaskRes{}

	consumer, err := sarama.NewConsumer([]string{kafka}, kafkaConfig)
	if err != nil {
		return task, err
	}
	defer consumer.Close()

	topic := "finished-str-tasks"
	partitionConsumer, err := consumer.ConsumePartition(topic, 0, sarama.OffsetNewest)
	if err != nil {
		return task, err
	}
	defer partitionConsumer.Close()

	for {
		msg := <-partitionConsumer.Messages()

		task = StrTaskRes{}

		json.Unmarshal(msg.Value, &task)

		if task.ID == targetTaskID {
			return task, nil
		}
	}
}
