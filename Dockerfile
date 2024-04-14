FROM python:3.9
WORKDIR /app

RUN pip install poetry
COPY ./ .
RUN poetry config virtualenvs.in-project true
RUN poetry install

COPY . /app
