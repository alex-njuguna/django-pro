# Pull base image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and requirements.txt
COPY Pipfile requirements.txt /code/

# Install dependencies
RUN pipenv install && pip install -r requirements.txt

# Copy project
COPY . /code/
