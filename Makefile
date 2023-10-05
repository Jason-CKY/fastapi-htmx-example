.DEFAULT_GOAL := help

# declares .PHONY which will run the make command even if a file of the same name exists
.PHONY: help
help:			## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.PHONY: lint
lint:			## Lint check
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --diff --parallel app

.PHONY: format
format:			## Format code in place to conform to lint check
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src odinuge/yapf:latest yapf \
	--style '{based_on_style: pep8, dedent_closing_brackets: true, coalesce_brackets: true}' \
	--no-local-style --verbose --recursive --in-place --parallel app

.PHONY: pyflakes
pyflakes:		## Pyflakes check for any unused variables/classes
	docker run --rm -v $(PWD):/src:Z \
	--workdir=/src python:3.8 \
	/bin/bash -c "pip install --upgrade pyflakes && python -m pyflakes /src && echo 'pyflakes passed!'"

.PHONY: build-dev
build-dev:		## rebuild all the images in the docker-compose file
	docker-compose -f docker-compose.dev.yml up --build -d

.PHONY: start-dev
start-dev:		## deploy app in dev environment with hot reloading
	docker-compose -f docker-compose.dev.yml up -d

.PHONY: stop-dev
stop-dev:		## bring down all hosted services
	docker-compose -f docker-compose.dev.yml down

.PHONY: destroy-dev
destroy-dev:		## Bring down all hosted services with their volumes
	docker-compose -f docker-compose.dev.yml down -v

.PHONY: build
build:		## rebuild all the images in the docker-compose file
	docker-compose up --build -d

.PHONY: start
start:		## deploy app
	docker-compose up -d

.PHONY: stop
stop:		## bring down all hosted services
	docker-compose down

.PHONY: destroy
destroy:		## Bring down all hosted services with their volumes
	docker-compose down -v
