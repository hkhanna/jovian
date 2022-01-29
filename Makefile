.PHONY: run app check all clean build db seed

include .env
SHELL := /bin/bash
DB_NAME = $(shell basename $(CURDIR))-db

# RUNNING AND TESTING #
run: 
	make app

app:
	@docker start ${DB_NAME}
	source .venv/bin/activate && python manage.py runserver ${WEB_PORT}

check:
	source .venv/bin/activate && py.test

# BUILD STEPS #
all: clean build seed 

clean:
	@echo "Removing python virtual environment"
	rm -rf .venv

build:
	@echo "Building python virtual environment"
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements/local.txt
	

db:
	@echo "Destroying postgres docker container"
	docker rm -f ${DB_NAME} || true

	@echo "Building postgres docker container"
	docker run --name ${DB_NAME} -e POSTGRES_HOST_AUTH_METHOD=trust -p ${DATABASE_PORT}:5432 -d postgres:13

# The port is forwarded from the standard postgres port (5432) to one that hopefully has no conflicts on the host.
# `-d` detaches the terminal from the container.
# `postgres:13` is intended to mirror the version of postgres available on Heroku.

	sleep 3
	@echo "Running migrations"
	source .venv/bin/activate && python manage.py migrate