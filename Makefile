#
# Makefile
#

#set default ENV based on your username and hostname
APP_DIR=api
TEST_DIR=tests
#get name of GIT branchse => remove 'feature/' if exists and limit to max 20 characters
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD | sed -r 's/[\/]+/-/g' | sed -r 's/feature-//g' | cut -c 1-20)
ENV ?= $(GIT_BRANCH)
AWS_DEFAULT_REGION ?= eu-west-1

#==========================================================================
# Test and verify quality of the app
serverless:
	#install serverless framework for Continous Deployment
	npm install -g serverless@2.66.1 || true
	sls plugin install -n serverless-python-requirements
	sls plugin install -n serverless-domain-manager
	pip install poetry
	touch $@


requirements: serverless
	poetry install
	touch $@

unittest: requirements
	poetry run pytest -s -vv

cov: requirements
	poetry run pytest --cov=${APP_DIR}

cov-html:
	poetry run coverage html

format: requirements
	poetry run isort $(APP_DIR)/**.py $(TEST_DIR)/**.py
	poetry run black $(APP_DIR) $(TEST_DIR)

lint: requirements
	poetry run pylint --version
	poetry run pylint ${APP_DIR} ${TEST_DIR}

isort: requirements
	poetry run isort --check-only $(APP_DIR)/**.py $(TEST_DIR)/**.py

black: requirements
	poetry run black --check $(APP_DIR) $(TEST_DIR)

security: requirements
	poetry run bandit --version
	poetry run bandit ${APP_DIR}

code-checks: isort black lint security

build:
	poetry run uvicorn api.main:app

deploy:
	@echo "======> Deploying to env $(ENV) <======"
ifeq ($(FUNC),)
	sls deploy --stage $(ENV) --verbose --region $(AWS_DEFAULT_REGION)
else
	sls deploy --stage $(ENV) -f $(FUNC) --verbose --region $(AWS_DEFAULT_REGION)
endif

run: requirements
	@echo "======> Running app on env $(ENV) <======"
	sls invoke --stage $(ENV) -f lambda_function1

sleep:
	sleep 5

logs: requirements
	@echo "======> Getting logs from env $(ENV) <======"
	sls logs --stage $(ENV) -f lambda_function1
	sls logs --stage $(ENV) -f lambda_function2

run-and-logs: run sleep logs

e2e-tests: requirements run-and-logs

load-tests: requirements
	@echo -e "load-tests not implemented yet"

destroy: requirements
	@echo "======> DELETING in env $(ENV) <======"
	sls remove --stage $(ENV) --verbose --region $(AWS_DEFAULT_REGION)

ci: code-checks unittest coverage
cd: ci deploy e2e-tests load-tests

.PHONY: e2e-test deploy destroy unittest coverage lint security code-checks run logs destroy
