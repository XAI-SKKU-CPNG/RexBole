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

# Enable git auto completion

git config --global --add safe.directory ${BASEDIR}
echo "source /usr/share/bash-completion/completions/git" >> ~/.bashrc


# Backend setup
cd $BASEDIR/apps/backend/

poetry install
poetry shell 
uvicorn --reload --host 127.0.0.1 --port 8000 app.main:app