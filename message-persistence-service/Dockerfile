FROM python:3.7-alpine
#RUN apk add mariadb-dev g++
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENTRYPOINT  [ "python", "kafka_service.py" ]
