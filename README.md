# Readme.md

This repo holds the L&D on how to create a proper gql backend for a simple application with jobs and employers. 

# How to run ? 

## Clone the repository. 

`git clone <repo link>`

## Setup your postgresDB

Create a posgtres DB with the following config. 

DATABASE_USER = "postgres"
DATABASE_PASSWORD = "admin"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "fastapi_graphene"

## Create the virtialenv using pipenv

RUN `pipenv install` 

## Activate the virtualenv

RUN `pipenv shell`

## Run the following command to run the app locally. 

RUN `uvicorn app.main:app --reload`

## Resources
## https://github.com/graphql-python/graphene/issues/545