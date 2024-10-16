# Проект с О!Хакатон
# Команда: Fullstack Excel
# Трек: Тегирование тарифов
## Демонстрация решения
1. [Видео с демонстрацией UI](https://drive.google.com/file/d/1HUae6sPYIHdbCdbew8UrupCY-CAXPMz9/view?usp=sharing)
2. [Презентация решения](https://github.com/ostrovok-hackathon-2024/fullstack-excel/blob/1c441ab47c09d58de207649f74998590c06d8e2d/presentation_FullStack.pdf)

## Докер приколы
Контейнер для гпу - DockerfileGPU

Контейнер для цпу - Dockerfile

Чтобы запустить:

docker build -f DockerfileGPU -t GPUtest

docker build -f Dockerfile -t test


## Небольшое уточнение

Из-за того что мы не могли со 100% уверенностью потрогать вашу виртуалку есть риски того, что будут проблемы с настройкой GPU. Если мы вдруг начнем помирать с километровыми логами - замените в app/requirements.txt 

```
optimum[onnxruntime-gpu]
onnxruntime-gpu
```

на 

```
optimum[onnxruntime]
onnxruntime
```

## Описание решения

Наше решение основано на использовании простых методов работы с текстом и ускорении языковых моделей с помощью **ONNX**. Мы не ограничились одной лишь моделью - мы написали веб-приложение с бэкендом на **Golang** для демонстрации взаимодействия с моделью и интеграции модели в ваши сервисы. Все это можно посмотреть и потрогать через фронтенд.

### Идея алгоритма

Как оказалось, на этой задаче очень хорошо работают такие методы как **Tf-Idf** и **Bag-of-Words** - в тарифах много информации в виде ключевых слов. Мы решили сделать линейные модели поверх этих преобразований бейзлайном нашего решения. Это Light-версия - она работает очень быстро с небольшой потерей в accuracy.

Дальше мы решили применить высоко оптимизированые модели на базе **BERT**. Для того, чтобы они работали быстрее, мы их квантизировали и запускали внутри **ONNX Runtime**. С достаточным (~2024) размером батча скорость работы в пересчете на 1 объект сравнима со скоростью Light-версии на одном объекте. Это Full-версия - она работает очень точно, но медленнее.

Хотелось бы написать пару слов про выбранную метрику accuracy. Большинство ошибок таких моделей есть `undefined` vs `<feature>`. Такие ошибки, в сущности, менее критичны, чем `<feature>` vs `<feature>`, что, к сожалению, accuracy не отражает. Поэтому наша модель работает лучше, чем об этом думает accuracy!

### Чистые и грязные данные

В грязных данных было много ошибок разметки, поэтому для обучения с учителем они не годились. Но на них можно было обучать токенайзеры и Tf-Idf! Так мы смогли извлечь из них выгоду.

Также пара примеров того как Full-вариант модели находит ошибки на грязном датасете:
| `rate_name` | `dirty['...']` | `predict` |
|--|--|--|
| Standard Single Bed in 8-Bed Dormitory Room (En Suite Share Bathroom) | suite (class) | dorm |
| Double Deluxe Flexible Room Only 200$ | run-of-house | room |

Пояснение: En Suite Bathroom - совмещенный санузел

### Анализ скорости

В `app/tests/test_speed.py` лежит бенчмарк. Замеры производились на датасете из 2400 строк внутри докер контейнера на умирающем ноутбуке без GPU, поэтому число OPS-ов нерепрезентативно. 


| Операция       | Single/Multiple | OPS (Light вариант) | OPS (Full вариант) |
|----------------|-----------------------------|------|----|
| Предобработка | single  | 901  | 820 | 
| Предсказание |    single   | 274 | 54 | 
| Предобработка | multiple  | 21 (50400/объект)  | 7.3 (17520/объект) |
| Предсказание | multiple  | 0.8 (1920/объект) | 0.09 (216/объект) |

## Как запускать

Чтобы запустить все вместе достаточно сделать `docker-compose up`. По отдельности:

### Модель

Модель можно поднять через `docker-compose -f docker-compose-app.yml up --build <variant>`, где `variant` это `app`или `app-gpu` 

Также мы написали accuracy и performance тесты для модели - их можно запустить `docker-compose -f docker-compose-test.yml up --build <variant>`, где `variant` это `test`или `test-gpu`

### Веб-приложение

Сделать `make up` в корневой директории

Можно использовать .env.example в /ml-test и в /backend, чтобы определить переменные для подключение к Kafka и PostgresSQL
Это нужно при запуске приложения не через `docker-compose`

## Другие комментарии

Мы подготовили ноутбуки для повторного обучения моделей. Их можно найти в папке `./model_trainer`
