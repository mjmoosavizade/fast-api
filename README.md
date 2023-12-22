# FastAPI Redis Application

This is a simple FastAPI application that uses Redis as a database.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- FastAPI
- aioredis
- Redis server

### Installing

1. Clone the repository

`git clone https://github.com/mjmoosavizade/fast-api.git`

2. Install the dependencies

`pip install requirements.txt`

3. Run the server

`uvicorn main:app --reload`


## Usage

The application provides the following endpoint:

- `POST /items/`: Create a new item. The body of the request should be a JSON object with the following structure:
  ``json
  {
 "name": "string",
 "description": "string"
  }


**Built With**

Built With
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [aioredis](https://github.com/aio-libs/aioredis) - Asynchronous Redis client
- [Redis](https://redis.io/) - In-memory data structure store

License
This project is licensed under the MIT License - see the LICENSE.md file for details