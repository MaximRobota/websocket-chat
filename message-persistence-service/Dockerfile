FROM python:3-onbuild

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "message_persistence_service.py" ]
