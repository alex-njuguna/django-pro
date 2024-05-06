# pull base image
from python:3.11

# set environment variables
env pythonunbuffered=1
env pythondontwritebytecode=1

# set working directory
workdir code/

# copy and install dependencies
copy requirements.txt
run pip install -r requirements.txt

# copy project
copy . /code/