#
# Makefile
#

#set default STAGE based on your username and hostname
APP_DIR=api
TEST_DIR=tests
#get name of GIT branchse => remove 'feature/' if exists and limit to max 20 characters
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD | sed -r 's/[\/]+/-/g' | sed -r 's/feature-//g' | cut -c 1-20)
GIT_TAG=$(shell git tag --points-at HEAD | cut -c 1-3)

STAGE ?= $(if $(GIT_TAG), $(GIT_TAG), $(GIT_BRANCH))

AWS_DEFAULT_REGION ?= eu-west-1

#==========================================================================
# Test and verify quality of the app
serverless:
	#install serverless framework for Continous Deployment
	npm install -g serverless@2.66.1 || true
	sls plugin install -n serverless-python-requirements
	sls plugin install -n serverless-domain-manager
	touch $@


requirements: serverless
	pip install poetry
	poetry env list
	poetry env info
	poetry install
	touch $@

unittest: requirements
	poetry run pytest -s -vv --ignore=node_modules $(TEST_FILE)

cov: requirements
	poetry run pytest -s -vv --ignore=node_modules --cov=${APP_DIR} $(TEST_FILE)

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
	poetry run uvicorn api.main:app --reload

deploy:
	@echo "======> Deploying to env $(STAGE) <======"
ifeq ($(FUNC),)
	sls deploy --stage $(STAGE) --verbose --region $(AWS_DEFAULT_REGION)
else
	sls deploy --stage $(STAGE) -f $(FUNC) --verbose --region $(AWS_DEFAULT_REGION)
endif

run: requirements
	@echo "======> Running app on env $(STAGE) <======"

logs: requirements
	@echo "======> Getting logs from env $(STAGE) <======"

run-and-logs: run logs

e2e-tests: requirements run-and-logs

load-tests: requirements
	@echo -e "load-tests not implemented yet"

destroy: requirements
	@echo "======> DELETING in env $(STAGE) <======"
	sls remove --stage $(STAGE) --verbose --region $(AWS_DEFAULT_REGION)

ci: code-checks unittest coverage
cd: ci deploy e2e-tests load-tests

.PHONY: e2e-test deploy destroy unittest coverage lint security code-checks run logs destroy
