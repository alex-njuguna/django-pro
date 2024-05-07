# pull base image
from python:3.11

# set environment variables
ENV PYTHONUNBUFFERD=1
ENV PYTHONDONTWRITEBYTECODE=1

# set working directory
workdir code/

# copy and run requirements
copy requirements.txt /code/
run pip install -r requirements.txt

# copy everything to the workdir
copy . /code/
