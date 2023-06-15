# Serverless python starter

This repository provide boilerplate for aws lambda.
The aws lambda is built by serverless-framework with python.

## Prerequisite

- asdf
- docker

# How to set up

- Run `make install`

# How to deploy

- If you want to deploy to localstack, run `docker compose up -d` beforehand

## How to deploy by serverless/compose(to localstack)

- Run `npx serverless deploy --stage {stage_name}`

## How to deploy by serverless(to localstack)

- Move service dir and run `npx serverless deploy --stage {stage_name}`

## NOTE

Please comment out functions.{function_name}.layers to deploy localstack(free edition)
