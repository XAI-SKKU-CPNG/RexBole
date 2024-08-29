#!/bin/bash

set -ex

BASEDIR=$(dirname $(dirname $(realpath $0)))


# Write .env file from .env.development
if [ -f .env ]
then
  rm .env
fi

while IFS= read -r line
do
  # Skip empty lines or comments
  if [[ -z "$line" || ${line:0:1} == '#' ]]
  then
    continue
  fi

  name=${line%%=*}
  value=${line#*=}

  if [[ -v "$name" ]]
  then
      echo "$name=${!name}" >> .env
  else
      echo "$name=$value" >> .env
  fi
done < .env.development


# Backend setup
cd $BASEDIR/apps/backend/

poetry install

# Let the DB start
poetry run python ./app/backend_pre_start.py

# Run migrations
poetry run alembic upgrade head

# Create initial data in DB
poetry run python ./app/initial_data.py
