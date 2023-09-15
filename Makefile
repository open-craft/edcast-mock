ensure-piptools:
	python -m pip install pip-tools

upgrade: ensure-piptools
	pip-compile requirements.in -o requirements.txt
	pip-compile requirements-dev.in -o requirements-dev.txt

requirements: ensure-piptools
	python -m piptools sync requirements.txt

dev: ensure-piptools
	python -m piptools sync requirements-dev.txt

up:
	docker compose up

