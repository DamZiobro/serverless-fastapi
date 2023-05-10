#
# Makefile
#

#set default STAGE based on your username and hostname
APP_DIR=api
TEST_DIR=tests
API_BASE_URL ?= http://localhost:8000

# Getting branch names for Git Flow
#get name of GIT branchse => remove 'feature/' if exists and limit to max 20 characters
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD | sed -r 's/[\/]+/-/g' | sed -r 's/feature-//g' | cut -c 1-20)
GIT_TAG=$(shell git tag --points-at HEAD | cut -c 1-3)

STAGE ?= $(if $(GIT_TAG), $(GIT_TAG), $(GIT_BRANCH))

AWS_DEFAULT_REGION ?= eu-west-1

#==========================================================================
# Test and verify quality of the app
serverless:
	#install serverless framework for Continous Deployment
	npm install -g serverless@3.15.2 || true
	sls plugin install -n serverless-python-requirements
	sls plugin install -n serverless-domain-manager
	sls plugin install -n serverless-localstack
	touch $@


deps: serverless
	@poetry --version &> /dev/null || (echo -e "ERROR: please install poetry" && false)
	poetry env list
	poetry env info
	poetry config virtualenvs.in-project true
	poetry install
	touch $@

unittest: deps
	poetry run pytest -s -vv --ignore=node_modules $(TEST_FILE)

cov: deps
	poetry run pytest -s -vv --ignore=node_modules --cov=${APP_DIR} $(TEST_FILE)

cov-html:
	poetry run coverage html

format: deps
	poetry run isort $(APP_DIR)/**.py $(TEST_DIR)/**.py
	poetry run black $(APP_DIR) $(TEST_DIR)

lint: deps
	poetry run flake8 --version
	poetry run flake8 ${APP_DIR} ${TEST_DIR}

isort: deps
	poetry run isort --check-only $(APP_DIR)/**.py $(TEST_DIR)/**.py

black: deps
	poetry run black --check $(APP_DIR) $(TEST_DIR)

security: deps
	poetry run bandit --version
	poetry run bandit ${APP_DIR}

code-checks: isort black lint security

run: deps ## run project in localhost web server
	poetry run uvicorn api.main:app --reload

deploy:
	@echo "======> Deploying to env $(STAGE) <======"
ifeq ($(FUNC),)
	sls deploy --stage $(STAGE) --verbose --region $(AWS_DEFAULT_REGION)
else
	sls deploy --stage $(STAGE) -f $(FUNC) --verbose --region $(AWS_DEFAULT_REGION)
endif

logs: deps
	@echo "======> Getting logs from env $(STAGE) <======"

e2e-tests: deps
	@echo "e2e-tests are NOT IMPLEMENTED YET"

load-tests: deps ## run load tests using locust tool (make run should be run in another terminal before)
	poetry run locust --headless -f tests/load/locustfile.py -H $(API_BASE_URL) --users 100 --spawn-rate 100 --run-time 30s

schema-tests: deps ## run API contract tests based on schemathesis tool (make run should be run in another terminal before)
	poetry run st run --checks all $(API_BASE_URL)/openapi.json

destroy: deps
	@echo "======> DELETING in env $(STAGE) <======"
	sls remove --stage $(STAGE) --verbose --region $(AWS_DEFAULT_REGION)

ci: code-checks unittest coverage
cd: ci deploy e2e-tests load-tests

clean:
	rm -rf .venv .coverage .serverless .pytest_cache serverless deps node_modules htmlcov __pycache__ .ruff_cache

.PHONY: e2e-test deploy destroy unittest coverage lint security code-checks run logs destroy
