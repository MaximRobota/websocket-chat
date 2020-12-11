FROM python:3.7-alpine
RUN apk add mariadb-dev libc-dev make git libffi-dev g++
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . /usr/src/app/

CMD [ "python", "identity_service.py" ]
#CMD [ "python", "-u", "identity_service.py" ]
