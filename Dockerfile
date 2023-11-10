FROM python:alpine

LABEL flask_blog latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENV FLASK_ENV "production"

CMD ["gunicorn", "src:create_app(mode='production')", "--bind", "0.0.0.0:8000"]
