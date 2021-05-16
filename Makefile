default: prompt

prompt:
	python3 -m tracker

py:
	python3

sh:
	bash

lint:
	python3 -m flake8 .

isort:
	python3 -m isort .

piprot:
	piprot

sure: lint isort piprot

test_on:
	pytest -vs ${ARGS}

tests:
	pytest -vs
.PHONY: tests

cov:
	pytest --cov=tracker

cov_html:
	pytest --cov=tracker --cov-report html:coverage_html

clean:
	rm -rf coverage_html
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf
