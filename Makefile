#!/bin/sh

run:
	docker compose up

test:
	docker compose -f ./docker-compose_test.yaml up

rm:
	docker rm -f flask_blog_backend flask_blog_db

rmi:
	docker rmi flask_blog postgres

app:
	docker rm -f flask_blog_backend flask_blog_db
	docker rmi flask_blog

clean:
	docker rm -f flask_blog_backend flask_blog_db
	docker rmi flask_blog postgres:alpine
