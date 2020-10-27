FROM python:3.7-alpine
RUN apk add mariadb-dev g++
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app/

CMD [ "python", "identity_service.py" ]
