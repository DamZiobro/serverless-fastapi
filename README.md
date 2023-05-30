## Serverless FastAPI-based API

**CI/CD status**:
![CI/CD](https://github.com/DamZiobro/serverless-fastapi/workflows/CI/CD/badge.svg)

This simple RESTful API project based on FastAPI is demonstration of multiple modern technologies/methodologies/principles:

  * **Python** programming language
    * RESTful API using [**FastAPI**](https://fastapi.tiangolo.com/lo/) framework
    * input data validation using [**pydantic**](https://docs.pydantic.dev/latest/) library
    * API designed using [Clean Architecture](https://www.freecodecamp.org/news/a-quick-introduction-to-clean-architecture-990c014448d2/) with help of [Repository Pattern](https://hackernoon.com/adopting-the-repository-pattern-for-enhanced-backend-development-with-fastapi)
    * [**poetry**](https://python-poetry.org/) for dependencies management
    * code checks using: **[flake8](https://flake8.pycqa.org/en/latest/), [black](https://pypi.org/project/black/), [isort](https://pycqa.github.io/isort/)**
    * unit tests using [**pytest**](https://docs.pytest.org/en/7.3.x/) and [hypothesis](https://hypothesis.readthedocs.io/en/latest/details.html)
    * code coverage using [**pytest-cov**](https://pypi.org/project/pytest-cov/)
    * load tests using [**locust**](https://locust.io/)
    * schema tests using [**schemathesis**](https://github.com/schemathesis/schemathesis)
    * contract tests using [**pact-python**](https://github.com/pact-foundation/pact-python)
  * cloud-based app deployed to **Amazon Web Services (AWS)**
  * **Serverless** (Serverless Framework) - AWS Lambda, API Gateway
  * **Microservices / serverless** architecture (AWS Lambdas creating REST API)
  * **Infrastracture as a Code** (IaaC) ([**Serverless framework**](https://www.serverless.com/framework/docs/getting-started) - [serverless.yml](serverless.yml) defines infrastructure resources)
  * **DevOps**-based workflow (common code base with [Makefile](Makefile) commands spanning Developers and Operations Teams together - used in CI/CD)
  * **CI/CD** pipeline
    * code syntax verification (flake8, isort, black) (`make lint`)
    * security verification (bandit) (`make security`)
    * unit tests (pytest) (`make unittest`)
    * code coverage (coverage python module)  (`make cov`)
    * deploy infrastructure (AWS, Serverless framework)  (`make deploy`)
    * End-To-End tests (behave, selenium, pytest-bdd) (NOT IMPLEMENTED YET) (`make e2e-tests`)
    * load/performance tests (locust) (`make load-tests`)
    * destroy infrastructure (AWS, Serverless framework)  (`make destroy`)
    * CI/CD deployment configured using [**Git Flow**](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) principles
  * **deploying from Command Line or from CI/CD** 
    * single Makefile to control all deployment and code checkings commands
    * available to **deploy to multiple stages /environments (ex. DEV, SIT, PROD)** using the same command (ex. `make deploy ENV=SIT`)
  * **Monitoring**
    * basic monitoring based on **CloudWatch Dashboards**
    * getting logs from **AWS CloudWatch**

This app template is based on [a Serverless Application Framework](https://www.serverless.com/)



### Quick start

#### Run locally

1. Install dependencies:
```
make deps
```
2. Run API locally:
```
make run
```
3. Check API is up and running by opening it's root URL [http://localhost:8000](http://localhost:8000) in your web browser.
4. Check [OpenAPI](https://swagger.io/specification/) docs is up and running by opening it's URL [http://localhost:8000/docs](http://localhost:8000/docs) in your web browser.

#### Deploy to AWS using Serverless Framework

1. [**Set up AWS credentials**](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) for your terminal
2. **Install Serverless Application Framework** via npm - [Instruction](https://www.serverless.com/framework/docs/getting-started#via-npm). You can use `make serverless` command from root directory of this project (or `sudo make serverless` if you see `EACCES: permission denied`).
3. **Deploy default app**
```
make deploy
```

Stages
----
You can work with app on specified stage (environment) ex. `dev`, `uat`, `prd` by passing ENV variable into the
`make` commands ex.:
```
make deploy ENV=dev
make deploy ENV=uat
make deploy ENV=prd 
```
or export `ENV` variable in your terminal and use default commands ex.
```
export ENV=dev
make deploy run
```

**The default stage for the app is equal to current branch name ex. master**. 

Building and deploying AWS resources
----
`make deploy` will build and deploy infrastructure and code as defined in [serverless.yml](serverless.yml) file:

By default resources are deployed to the default
[stage](https://serverless-stack.com/chapters/stages-in-serverless-framework.html)
(environment) based on current branch name ex. `master`. Thanks to that multiple users working on separate branches can deploy to
separate AWS resources to avoid resources conflicts.

Tests
----
We have following level of tests in the application:
- `make code-checks` - checks code syntax using `flake8`, `black`, `isort` and security using `bandit` 
- `make unittest cov` - trigger all unit tests of the code and show code coverage
- `make e2e-tests` (NOT IMPLEMETED YET) - behave-based tests runned after deployment
- `make schema-tests` - schemathesis-based API schema tests
- `make contract-tests` - pact-based API contract tests
- `make load-tests` - locust-based load tests

CI/CD
----
The CI/CD is based on Makefile targets and is integrated with GitHub Actions to
trigger (however it could be easly integrated with any other CI/CD tool ex. 
Jenkins, BitBucket pipelines, GitLab, TravisCI, Bamboo or any other)

It consists of following steps:

Continous Integration
--------
You can run all the below steps/commands using one `make ci` command
- `make lint` => check code syntax using `pylint` tool
- `make security` => check code security breaches using `bandit` tool
- `make unittest` => trigger unit tests and show report
- `make cov` => show unit tests code coverage

Continous Deployment
--------
You can run all the below steps/commands using one `make cd` command:
- `make deploy` => deploys app to AWS
- `make e2e-tests` => run End to End tests on deployed app
- `make load-tests` => run Load tests on deployed app
- `make destroy` => (optional: works only on GitFlow feature branches) destroy AWS
  resources after finishing e2e-tests


CI/CD pipelines
--------
Currently CI/CD is integrated with GitHub Actions. However you can set it up
quickly with any other CI/CD tool and see pipelines and actions similar to the
ones below.

To run CI/CD pipelines you need to export `AWS_KEY` and `AWS_SECRET` to the
`Secrets` section of your GitHub project:
![](docs/pipelines-secrets-setup.png)

**You can see CI/CD pipelines of project** [here](https://github.com/DamZiobro/serverless-aws-lambda-sqs-app/actions)

Pipelines of GitHub Actions looks like on this picture:
![](docs/pipelines.png)

Pipeline steps are configured in [pipeline config file](.github/workflows/cicd.yml)

Sample pipeline processing with details of each step can be found when you
click on some of the pipelines in [Actions tab](https://github.com/DamZiobro/serverless-aws-lambda-sqs-app/actions).

It should look like on this picture:
![](docs/pipeline-details.png)


Code syntax formatting
----
We can automatically reformat the code according to black and isort rules:
```
make format
```

Creating and Merging Pull Requests according to GitFlow
--------

To create Pull Request, go to [Pull Requests](https://github.com/DamZiobro/serverless-aws-lambda-sqs-app/pulls) and
fo following steps: 
1. Click 'New pull request'
2. Select your branch and click on it.
3. Make sure you selected your PR to be merged into `develop` (NOT `master`)
   (we will use GitFlow for releases later)
4. Click create Pull Request

When you follow above actions, the CI/CD pipeline will be triggered automatically and perform all checkings described in CI/CD section above.

When everything will be finished you should see results like here and if
everything is green you can ask your colleague for Code Review. 

If something is not green, you should fix it before asking Code Review.
![](docs/pipeline-checkings.png)

When you Code is reviewed you can click 'Merge pull request' and merge it into
`develop` branch.
