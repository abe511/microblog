FROM python:alpine

LABEL flask_blog latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 80

ENV FLASK_ENV "development"

CMD ["flask", "run"]

