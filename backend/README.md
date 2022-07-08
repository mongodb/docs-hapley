# Hapley Backend API

## Local Development

### Requirements and Installation

Make sure to have the following installed:

- python v3.10+
- [pipenv](https://pipenv.pypa.io/en/stable/#install-pipenv-today) - for dependency management

Run the following command from the `backend/` directory to install all current dependencies.

```
pipenv install --dev
```

If you have `pipenv` installed but your local machine can't run the command, try running:

```
python3 -m pipenv install --dev
```

The `--dev` option allows both production and dev packages to be installed.

### Running Locally

```
uvicorn main:app --reload
```

Go to http://127.0.0.1:8000/ to access routes. If you'd prefer to host the API on a different port, run the above command with the `--port=<int>` flag.

> :bulb: Note: The frontend uses port 3000 for hosting.

### Running in a Docker Container

If you'd like to develop locally using Docker, ensure that you have Docker installed on your machine. You can download and install Docker [here](https://docs.docker.com/get-docker/).

Run the following commands from the `backend` directory:

```
docker build --tag hapley-backend .
docker run -dp 8000:8000 hapley-backend
```

The above commands will create and tag an image using the Dockerfile found in the `backend` directory. The image is then ran into a container for local development.

Go to http://127.0.0.1:8000/ to access routes.

(TODO: Update instructions for Docker Compose and consolidate with frontend.)

### Accessing OpenAPI Docs

FastAPI has a feature that generates an OpenAPI schema. The schema can be found on http://127.0.0.1:8000/openapi.json. Go to http://127.0.0.1:8000/docs if you'd prefer to see the API documentation interactively.

Additional information about FastAPI's OpenAPI generation can be found [here](https://fastapi.tiangolo.com/tutorial/first-steps/#openapi).

## Testing

To be added in future PR.

## Linting and Styling

To be added in future PR.

## FastAPI Resources

- [Documentation](https://fastapi.tiangolo.com/)
