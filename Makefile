install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv --cov=poker --cov-report=term-missing tests/

format:
	black src/poker tests/

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py src/poker

container-lint:
	docker run --rm -i hadolint/hadolint < .devcontainer/Dockerfile

refactor: format lint

deploy:
	#deploy goes here

all: install lint test format deploy
