.PHONY: help install test run docker-up docker-build format

help:
	@echo "Make targets:"
	@echo "  make install    # create venv and install requirements"
	@echo "  make test       # run unit tests"
	@echo "  make run        # run the flask dev server"
	@echo "  make docker-up  # run with docker-compose"
	@echo "  make docker-build # build docker image"

install:
	python3 -m venv .venv || true
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

test:
	PYTHONPATH=src pytest -q

run:
	python3 web/app.py

docker-up:
	docker compose up --build

docker-build:
	docker build -t codexrpg:latest .
