import polars as pl
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tqdm.notebook import tqdm
import os
import pickle
import json
import re
from tabulate import tabulate
from typing import List, Dict, Any


# Установите переменную окружения
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'


class TransformerModelTrainer:
    def __init__(self, model_name: str, label_columns: List[str]) -> None:
        self.model_name = model_name
        self.label_columns = label_columns
        self.label_encoders = {}
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def substitute_non_standard_digits(self, input_string: str) -> str:
        '''Заменяет нестандартные цифры на стандартные в строке'''
        non_standard_to_standard = {
            '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
            '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
            '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
            '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
            '零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
            '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
            '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
            '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
        }
        translation_table = str.maketrans(non_standard_to_standard)
        return input_string.translate(translation_table)

    def preprocess_text(self, text: str) -> str:
        '''Предобрабатывает текст: удаляет символы и приводит к нижнему регистру'''
        if isinstance(text, str):
            text = self.substitute_non_standard_digits(text)
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text.lower().strip()
        return None

    def process(self, df: pl.DataFrame) -> pl.DataFrame:
        '''Обрабатывает DataFrame: чистит текстовые данные и заполняет пропуски'''
        proc = df[['rate_name'] + self.label_columns].to_pandas()
        proc['rate_name'] = proc['rate_name'].map(self.preprocess_text)
        proc['bedding'] = proc['bedding'].replace('twin/twin-or-double', 'double/double-or-twin')
        for col in self.label_columns:
            proc[col].fillna('undefined', inplace=True)
        return proc.dropna(subset=['rate_name'])

    def encode_labels(self, df: pl.DataFrame) -> pl.DataFrame:
        '''Кодирует метки с помощью LabelEncoder и сохраняет их'''
        for label in self.label_columns:
            le = LabelEncoder()
            df[label] = le.fit_transform(df[label])
            self.label_encoders[label] = le
            with open(f'label_encoder_{label}.pkl', 'wb') as f:
                pickle.dump(le, f)
        return df

    def tokenize_function(self, examples: Dict[str, Any]) -> Dict[str, Any]:
        '''Токенизирует текст'''
        return self.tokenizer(examples['rate_name'], padding="max_length", truncation=True, max_length=128)

    def prepare_labels(self, examples: Dict[str, Any], label_column: str) -> Dict[str, Any]:
        '''Подготавливает метки для тренировки'''
        examples['label'] = examples[label_column]
        return examples

    def compute_metrics(self, p: Any) -> Dict[str, float]:
        '''Вычисляет метрики'''
        preds = p.predictions.argmax(-1)
        labels = p.label_ids
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro', zero_division=0)
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }

    def train_and_evaluate_model(self, label_column: str) -> Dict[str, Any]:
        '''Тренирует и оценивает модель для заданной метки'''
        print(f"Evaluating: {label_column}")
        tokenized_datasets = self.datasets.map(self.tokenize_function, batched=True)
        tokenized_datasets = tokenized_datasets.map(lambda x: self.prepare_labels(x, label_column), batched=True)
        tokenized_datasets.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

        labels = np.array(tokenized_datasets['train']['label'])
        class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(labels), y=labels.flatten())
        class_weights = torch.tensor(class_weights, dtype=torch.float)

        model = AutoModelForSequenceClassification.from_pretrained(self.model_name,
                                                                   num_labels=len(np.unique(labels)),
                                                                   problem_type="single_label_classification")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        training_args = TrainingArguments(
            output_dir=f'./results/{label_column}',
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=128,
            num_train_epochs=50,
            weight_decay=0.01,
            logging_dir=f'./logs/{label_column}',
            logging_steps=10,
            report_to='none',
            save_total_limit=1,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
            overwrite_output_dir=True
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets['train'],
            eval_dataset=tokenized_datasets['val'],
            compute_metrics=self.compute_metrics
        )

        train_results = trainer.train()
        best_model_path = trainer.state.best_model_checkpoint
        best_model = AutoModelForSequenceClassification.from_pretrained(best_model_path)
        best_model.to(device)

        trainer.model = best_model
        eval_results = trainer.evaluate(tokenized_datasets['test'])

        return {
            'label_column': label_column,
            'best_model_path': best_model_path,
            'eval_results': eval_results
        }

    def train_and_evaluate(self, df: pl.DataFrame) -> Dict[str, Dict[str, Any]]:
        '''Тренирует и оценивает модели для каждой категории'''
        df_processed = self.process(df)
        df_processed = self.encode_labels(df_processed)

        train_df, temp_df = train_test_split(df_processed, test_size=0.4, random_state=42)
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

        train_dataset = Dataset.from_pandas(train_df)
        val_dataset = Dataset.from_pandas(val_df)
        test_dataset = Dataset.from_pandas(test_df)

        self.datasets = DatasetDict({
            'train': train_dataset,
            'val': val_dataset,
            'test': test_dataset
        })

        results = {}
        for label_column in tqdm(self.label_columns, desc=f"Training model"):
            result = self.train_and_evaluate_model(label_column)
            results[label_column] = result

        with open('results.json', 'w') as f:
            json.dump(results, f, indent=4)

        print("Training and evaluation completed. Results saved to results.json")
        return results

    def print_results(self, results: Dict[str, Dict[str, Any]]) -> None:
        '''Выводит результаты в табличном формате'''
        headers = ["Label Column", "Best Model Path", "Accuracy", "F1 Score", "Precision", "Recall"]
        rows = []

        for label_column, result in results.items():
            best_model_path = result['best_model_path']
            eval_results = result['eval_results']
            rows.append([
                label_column,
                best_model_path,
                eval_results['eval_accuracy'],
                eval_results['eval_f1'],
                eval_results['eval_precision'],
                eval_results['eval_recall']
            ])

        print(tabulate(rows, headers=headers, tablefmt="pipe"))

# Usage example
# trainer = TransformerModelTrainer(model_name='TaylorAI/bge-micro-v2', label_columns=["bedding", "capacity", "bedrooms", "view"])
# data_clean = pl.read_csv("PATH_TO_DATASET")
# results = trainer.train_and_evaluate(data_clean)
# trainer.print_results(results)