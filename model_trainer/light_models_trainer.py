import re
import pandas as pd
import warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from tqdm import tqdm
import optuna
import pickle
import sys
import os
from typing import List, Tuple, Dict, Any

# warnings.filterwarnings("ignore")
# sys.stderr = open(os.devnull, 'w')

class ModelTrainer:
    def __init__(self) -> None:
        '''Инициализация словаря с категориями для отелей'''
        self.categories_dict: Dict[str, List[str]] = {
            "class": ["run-of-house", "dorm", "capsule", "room", "junior-suite", "suite", "apartment", "studio", "villa", "cottage", "bungalow", "chalet", "camping", "tent"],
            "quality": ["undefined", "economy", "standard", "comfort", "business", "superior", "deluxe", "premier", "executive", "presidential", "premium", "classic", "ambassador", "grand", "luxury", "platinum", "prestige", "privilege", "royal"],
            "bathroom": ["undefined", "shared bathroom", "private bathroom", "external private bathroom"],
            "bedding": ["undefined", "bunk bed", "single bed", "double/double-or-twin", "twin/twin-or-double", "multiple"],
            "capacity": ["undefined", "single", "double", "triple", "quadruple", "quintuple", "sextuple"],
            "bedrooms": ["undefined", "1 bedroom", "2 bedrooms", "3 bedrooms", "4 bedrooms", "5 bedrooms", "6 bedrooms"],
            "club": ["not club", "club"],
            "balcony": ["no balcony", "with balcony"],
            "view": ["undefined", "bay view", "bosphorus view", "burj-khalifa view", "canal view", "city view", "courtyard view", "garden view", "golf view", "harbour view", "lake view", "land view", "mountain view", "ocean view", "panoramic view", "park view", "partial-ocean view", "pool view", "river view", "sea view", "street view", "sunrise view", "sunset view", "water view", "with view", "beachfront", "ocean front", "sea front"],
            "floor": ["undefined", "penthouse floor", "duplex floor", "basement floor", "attic floor"]
        }

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

    def process(self, df: pd.DataFrame, target_columns: List[str]) -> pd.DataFrame:
        '''Обрабатывает DataFrame: чистит текстовые данные и заполняет пропуски'''
        proc = df[['rate_name'] + target_columns].copy()
        proc['rate_name'] = proc['rate_name'].map(self.preprocess_text)
        proc['bedding'] = proc['bedding'].replace('twin/twin-or-double', 'double/double-or-twin')
        for col in target_columns:
            proc[col].fillna('undefined', inplace=True)
        return proc.dropna(subset=['rate_name'])

    def save_model_and_vectorizer(self, model: Any, vectorizer: Any, category_name: str) -> None:
        '''Сохраняет модель и векторайзер в файлы'''
        with open(f'{category_name}_model.pkl', 'wb') as model_file:
            pickle.dump(model, model_file)
        with open(f'{category_name}_vectorizer.pkl', 'wb') as vec_file:
            pickle.dump(vectorizer, vec_file)

    def perform_optuna_search(self, X_train: pd.Series, y_train: pd.Series,
                              tfidf_vectorizer: TfidfVectorizer, count_vectorizer: CountVectorizer) -> Tuple[Any, Any, Dict[str, Any]]:
        '''Выполняет подбор гиперпараметров с использованием Optuna'''
        def objective(trial: optuna.Trial) -> float:
            vectorizer_type = trial.suggest_categorical('vectorizer_type', ['tfidf', 'count'])
            if vectorizer_type == 'tfidf':
                vectorizer = tfidf_vectorizer
            else:
                vectorizer = count_vectorizer

            model_type = trial.suggest_categorical('model_type', ['logreg', 'svc', 'linsvc'])

            if model_type == 'logreg':
                penalty = trial.suggest_categorical('penalty', ['l2'])
                solver = trial.suggest_categorical('solver', ['lbfgs', 'liblinear'])
                C = trial.suggest_loguniform('C', 1e-2, 1e2)
                model = LogisticRegression(penalty=penalty, solver=solver, C=C, max_iter=1000)

            elif model_type == 'svc':
                C = trial.suggest_loguniform('C', 1e-2, 1e2)
                kernel = trial.suggest_categorical('kernel', ['linear', 'rbf'])
                model = SVC(C=C, kernel=kernel, class_weight='balanced')

            else:  # LinearSVC
                C = trial.suggest_loguniform('C', 1e-2, 1e2)
                model = LinearSVC(C=C, max_iter=2000, class_weight='balanced')

            model.fit(vectorizer.transform(X_train), y_train)
            accuracy = model.score(vectorizer.transform(X_train), y_train)

            trial.set_user_attr('model', model)
            trial.set_user_attr('vectorizer', vectorizer)

            return accuracy

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=20)

        best_trial = study.best_trial
        return best_trial.user_attrs['model'], best_trial.user_attrs['vectorizer'], best_trial.params

    def evaluate_model(self, model: Any, X_test: pd.Series, y_test: pd.Series, vectorizer: Any) -> Tuple[float, float, float, float]:
        '''Оценивает модель и возвращает метрики'''
        y_pred = model.predict(vectorizer.transform(X_test))
        print(classification_report(y_test, y_pred, digits=5))

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        return accuracy, precision, recall, f1

    def train_and_evaluate(self, df_train: pd.DataFrame, df_test: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        '''Тренирует и оценивает модели для каждой категории'''
        metrics_results: Dict[str, Dict[str, float]] = {}

        tfidf_vectorizer = TfidfVectorizer()
        count_vectorizer = CountVectorizer()

        # Обучение векторайзеров на тренировочных данных
        tfidf_vectorizer.fit(df_train['rate_name'].astype(str).values)
        count_vectorizer.fit(df_train['rate_name'].astype(str).values)

        for category in tqdm(self.categories_dict.keys(), desc="Training categories"):
            X_train = df_train['rate_name'].astype(str).values
            y_train = df_train[category.lower()].astype(str).values
            X_test = df_test['rate_name'].astype(str).values
            y_test = df_test[category.lower()].astype(str).values

            best_model, best_vectorizer, best_params = self.perform_optuna_search(X_train, y_train, tfidf_vectorizer, count_vectorizer)

            self.save_model_and_vectorizer(best_model, best_vectorizer, category)

            accuracy, precision, recall, f1 = self.evaluate_model(best_model, X_test, y_test, best_vectorizer)
            metrics_results[category] = {
                'accuracy': round(accuracy, 5),
                'precision': round(precision, 5),
                'recall': round(recall, 5),
                'f1': round(f1, 5)
            }

        return metrics_results

    def print_metrics(self, metrics_results: Dict[str, Dict[str, float]]) -> None:
        '''Выводит метрики для каждой категории'''
        for category, metrics in metrics_results.items():
            print(f"\nMetrics for {category}:")
            print(f"{'-' * 30}")
            print(f"Accuracy: {metrics['accuracy']:.5f}")
            print(f"Precision: {metrics['precision']:.5f}")
            print(f"Recall: {metrics['recall']:.5f}")
            print(f"F1 Score: {metrics['f1']:.5f}")
            print(f"{'-' * 30}")


# Usage example
# trainer = ModelTrainer()
# df = pd.read_csv(r"D:\rates_clean_train.csv")
# targets = ["class", "quality", "bathroom", "bedding", "capacity", "bedrooms", "club", "view"]
# df_processed = trainer.process(df, targets)
# df_train, df_test = train_test_split(df_processed, test_size=0.2, random_state=42)
# metrics = trainer.train_and_evaluate(df_train, df_test)
# trainer.print_metrics(metrics)