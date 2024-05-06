# pull base image
from python:3.11

# set environment variables
env PYTHONUNBUFFERD=1
env PYTHONDONTWRITEBYTECODE=1

# set working directory
workdir code/

# copy and install dependencies
copy requirements.txt /code/
run pip install -r requirements.txt

# copy project
copy . /code/