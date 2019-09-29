SHELL := /usr/bin/env bash

.PHONY: deps
deps:
	pip install --upgrade pip setuptools
	pip install -r requirements.txt

.PHONY: run
run:
	python app/app.py