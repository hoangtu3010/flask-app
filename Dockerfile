FROM --platform=linux/amd64 python:3.8-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD waitress-serve --listen 0.0.0.0:$PORT wsgi:application