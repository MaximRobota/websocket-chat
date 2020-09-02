FROM python:3-onbuild

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt && pip install --upgrade pip

CMD [ "python", "message-persistence-service.py" ]
