
# Crypto Price Client & API

This project contains two  components:
- **Client**: Fetches cryptocurrency prices (BTC/USD, ETH/USD) from the Deribit API every minute and stores them in a SQLite database.
- **API**: A FastAPI server that provides endpoints to access saved price data.

## Table of Contents
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)

---

## Installation

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/giveuper39/hh_test_crypto
   cd hh_test_crypto
   ```

2. **Build Docker Containers**
   ```bash
   docker compose build
   ```

---

## Running the Application

To run the client and API simultaneously:

```bash
docker-compose up client api
```

- **Client**: Fetches prices and updates the SQLite database.
- **API**: Starts a FastAPI server at `http://localhost:8000`.

### Stopping the Application

```bash
docker-compose down
```

---

## Running Tests

To run all tests using Docker:

```bash
docker compose run --rm test
```

Alternatively, to run tests locally with Poetry:
```bash
make test
```

---

## API Documentation

Once the API is running, documentation for the available endpoints can be found at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### API Endpoints

#### 1. Get All Prices by Currency
- **Endpoint**: `/prices`
- **Method**: `GET`
- **Query Params**: `ticker` (required, e.g., `btc_usd`)
- **Description**: Retrieve all saved prices for a specified ticker.

#### 2. Get Latest Price for a Currency
- **Endpoint**: `/prices/latest`
- **Method**: `GET`
- **Query Params**: `ticker` (required, e.g., `eth_usd`)
- **Description**: Retrieve the latest price entry for a specified ticker.

#### 3. Get Prices by Date Range
- **Endpoint**: `/prices/by_date`
- **Method**: `GET`
- **Query Params**: `ticker` (required), `start_date`, `end_date` (format: `dd-mm-yyyy`)
- **Description**: Retrieve prices for a specified ticker within a date range.

