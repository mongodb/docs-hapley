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

#### Generating a JWT Token
The API implements middleware that validates incoming JWT tokens are associated with users who belong to authorized Okta groups. Follow these steps to generate a fake JWT token that can be used for local development:

1. Create a `.env` file within the backend directory.
2. Start the local development server with `pipenv run app`
3. Using Postman, `cURL`, or a similar tool, send a request to the `/api/v1/sample-token` endpoint with `username` and `email` query parameters. For example: `http://localhost:8000/api/v1/sample-token?email=foo@mongodb.com&username=foo`
4. Create a `JWT_TOKEN` environment variable in `.env`. Set this equal to the token received in the JSON response.
5. Shut down the development server with Ctrl + C

#### Database Connection

We provide two options for database connection while working locally. You can either connect to a local instance of `mongod` or you can connect to an Atlas database. We will provide instructions for both.

**Connecting to Mongo Locally**:

Before you begin these steps, ensure that you've installed the MongoDB database and shell on your computer. You can find instructions for installing MongoDB [here](https://www.mongodb.com/docs/manual/installation/) and instructions for installing `mongosh` [here](https://www.mongodb.com/docs/mongodb-shell/install/). You'll want to install the free MongoDB Community Edition.

After installing MongoDB, don't forget to run it to start the `mongod` process. The command for running on macOS would be `brew services start mongodb-community@<version #>`.

To verify that the installations were successful, run the command `mongosh`. The Mongo shell should connect to your local `mongod` process automatically.

Now you're ready to seed your database locally. Follow these steps:
1. From the `backend` repository, run `ATLAS_USERNAME=<username-here> ./db_seed`. `ATLAS_USERNAME` should be the database username you normally use to connect to the docs platform cluster.
2. The `db_seed` script will prompt you for your database password twice.
3. After entering your password twice, the script will download data from Atlas and load it into your local MongoDB instance.

You should now have seed data in collections called `entitlements` and `repos_branches` within a `hapley-dev` database. You can verify setup worked correctly by connecting to `mongodb://localhost:27017` in Compass.

Finally, add `MONGO_URI` and `MONGO_DB_NAME` to your `.env` file. `MONGO_URI` should be set to `mongodb://localhost:27017`, and `MONGO_DB_NAME` should equal `hapley-dev`.

**Connecting via Atlas**:

If you'd like to develop using sample data in Atlas, set `MONGO_URI` in your `.env` file to `mongodb+srv://<db-username>:<db-password>@cluster0.ylwlz.mongodb.net`, and set `MONGO_DB_NAME` to `hapley-dev`.

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

#### Testing in API Client

If you want to send requests to the Hapley API from an API tool such as **Postman**, you'll need to mock the cookies traditionally attached to requests via CorpSecure. For example, if you send a `GET` request to `http://localhost:8000/api/v1`, the request headers must contain a key `cookie` with a value of `auth_user=<mongo-username>; auth_token=<jwt-token>` where `jwt-token` is the token generated via a request to `/api/v1/sample-token` and `mongo-username` equals the `username` query parameter passed to `/api/v1/sample-token`.

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

All tests are located in the `api/tests/` directory and can be run with `pipenv` and
`pytest`.

From the `backend/` directory, use the following to run all tests:

```
pipenv run test
```

To run all tests within a specific file:

```
pipenv run test -- api/tests/path/to/test.py
```

To run a specific test:

```
pipenv run test -- api/tests/path/to/test.py::test_name
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
