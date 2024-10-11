FROM python:3.10-slim

WORKDIR /opt

COPY app/requirements*.txt app/

RUN pip3 install --no-cache-dir -r app/requirements.txt
RUN pip3 install --no-cache-dir -r app/requirements-cpu.txt

COPY app app

ENTRYPOINT ["python3", "./app/app.py"]
