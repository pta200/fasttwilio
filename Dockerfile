# pull official base image
FROM python:3.12-slim

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy only the dependency files
COPY pyproject.toml poetry.lock ./


#install python dependencies
RUN pip install poetry; poetry config virtualenvs.create false; poetry install --no-root --no-interaction --no-ansi

# copy app
COPY . .

ENTRYPOINT [ "./run_service.sh"]