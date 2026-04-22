# FastTwilio

FastAPI Service to lean Mongo, FastAPI, and Twilio SMS API

## Development
The repos uses [poetry](https://python-poetry.org/) for dependency management, building. Use the docker compose to run the service.

This will allow you to see the OpenAPI (Swagger) inter fact as http://localhost:8000/docs.
```bash
$ sudo docker compose up -d --build
```

## Tests
To run the tests run the following
```bash
$ poetry run pytest
```

## License

[MIT](https://choosealicense.com/licenses/mit/)