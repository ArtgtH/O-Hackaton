FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y make gcc && \
    apt-get clean

WORKDIR /ml
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt && rm requirements.txt

COPY . .

CMD ["python", "src/starter.py"]