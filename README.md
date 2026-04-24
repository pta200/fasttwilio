# FastTwilio

FastAPI service to lean Mongo, FastAPI, and Twilio SMS API as part of a notifcation application

## Development
The repos uses [poetry](https://python-poetry.org/) for dependency management, building. Use docker compose to run the service.

This will allow you to see the OpenAPI (Swagger) inter fact as http://localhost:8000/docs.
```bash
$ sudo docker compose up -d --build
```

## Tests
To run the tests make sure to add values to the devopment.env file and run the following command
```bash
$ poetry install
$ poetry run pytest
```

## Security
To run Bandit to find common security issues in Python code. 
```bash
bandit -c pyproject.toml -r .
```

To run pip-audit package vulnerabilities
```bash
poetry run pip-audit
```


## License

[MIT](https://choosealicense.com/licenses/mit/)