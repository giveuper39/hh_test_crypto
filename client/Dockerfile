FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app
RUN apt update && apt install make
RUN pip install poetry && poetry install

COPY . /app

CMD ["make", "run_client"]
