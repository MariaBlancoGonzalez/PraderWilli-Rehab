.PHONY: venv install run clean

SHELL := /bin/bash

all: install run

venv:
	python3 -m virtualenv .

run:
	python3 src/main.py