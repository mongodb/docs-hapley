# Hapley Backend API

## Local Development

### Requirements and Installation

Make sure to have the following installed:

- python v3.10+
- [pipenv](https://pipenv.pypa.io/en/stable/#install-pipenv-today) - for
dependency management

Run the following command from the `backend/` directory to install all current
dependencies.

```
pipenv install --dev
```

If you have `pipenv` installed but your local machine can't run the command, try
running:

```
python3 -m pipenv install --dev
```

The `--dev` option allows both production and dev packages to be installed.

### Running Locally

**Generating a JWT Token**:
The API implements middleware that validates incoming JWT tokens are associated with users who belong to authorized Okta groups. Follow these steps to generate a fake JWT token that can be used for local development:

1. Create a `.env` file within the backend directory.
2. Start the local development server with `pipenv run app`
3. Using Postman, `cURL`, or a similar tool, send a request to the `/api/v1/sample-token` endpoint with `username` and `email` query parameters. For example: `http://localhost:8000/api/v1/sample_token?email=foo@mongodb.com&username=foo`
4. Create a `JWT_TOKEN` environment variable in `.env`. Set this equal to the token received in the JSON response.
5. Shut down the development server with Ctrl + C

**Seeding the Database**:

Before you begin these steps, ensure that you've installed the MongoDB database and shell on your computer. You can find instructions for installing MongoDB [here](https://www.mongodb.com/docs/manual/installation/) and instructions for installing `mongosh` [here](https://www.mongodb.com/docs/mongodb-shell/install/).

After installing MongoDB, don't forget to run it to start the `mongod` process. The command for running on macOS would be `brew services start mongodb-community@<version #>`.

To verify that the installations were successful, run the command `mongosh`. The Mongo shell should connect to your local `mongod` process automatically.

Now, `cd` into the `seed` directory and run `./load`. This loads seed data from two JSON files into collections called `entitlements` and `repos_branches` within a `hapley-dev` database.

Finally, add `MONGO_URI` and `MONGO_DB_NAME` to your `.env` file. `MONGO_URI` should be set to `mongodb://localhost:27017`, and `MONGO_DB_NAME` should equal `hapley-dev`.

**Starting the Server**:

Now, restart the development server with:
```
pipenv run app
```

Go to http://127.0.0.1:8000/api/v1 to access routes. To host the API on a different
port, run:

```
pipenv run -- app --port=<int>
```

> :bulb: Note: The frontend uses port 3000 for hosting.

### Running in a Docker Container

If you'd like to develop locally using Docker, ensure that you have Docker
installed on your machine. You can download and install Docker
[here](https://docs.docker.com/get-docker/).

Run the following commands from the `backend` directory:

```
docker build --tag hapley-backend .
docker run -dp 8000:8000 hapley-backend
```

The above commands will create and tag an image using the Dockerfile found in
the `backend` directory. The image is then ran within a container for local development.

Go to http://127.0.0.1:8000/api/v1 to access routes.

(TODO: Update instructions for Docker Compose and consolidate with frontend.)

### Accessing OpenAPI Docs

FastAPI has a feature that generates an OpenAPI schema. The schema can be found
on http://127.0.0.1:8000/api/v1/openapi.json. Go to http://127.0.0.1:8000/api/v1/docs if you'd prefer to see the API documentation interactively.

Additional information about FastAPI's OpenAPI generation can be found
[here](https://fastapi.tiangolo.com/tutorial/first-steps/#openapi).

## Testing

All tests are located in the `tests/` directory and can be run with `pipenv` and
`pytest`.

From the `backend/` directory, use the following to run all tests:

```
pipenv run test
```

To run all tests within a specific file:

```
pipenv run test -- tests/path/to/test.py
```

To run a specific test:

```
pipenv run test -- tests/path/to/test.py::test_name
```

See the [pytest docs](https://docs.pytest.org/en/7.1.x/how-to/usage.html) for
more information on usage.

## Linting and Styling

The backend uses [black](https://black.readthedocs.io/en/stable/) for formatting
and [flake8](https://flake8.pycqa.org/en/latest/) for linting. Run the following
commands to format and lint locally.

```
pipenv run format
pipenv run lint
```

## FastAPI Resources

- [Documentation](https://fastapi.tiangolo.com/)
