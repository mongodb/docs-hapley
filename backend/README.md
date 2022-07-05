# Hapley Backend API

## Local Development

### Requirements and Installation

Make sure to have the following installed:

- python v3.10+
- [pipenv](https://pipenv.pypa.io/en/stable/#install-pipenv-today) - for dependency management

Run the following command from the `backend/` directory to install all current dependencies.

```
pipenv install
```

If you have `pipenv` installed but your local machine can't run the command, try running:

```
python3 -m pipenv install
```

### Running Locally

```
uvicorn main:app --reload
```

Go to `http://127.0.0.1:8000/` to access routes.

## Testing

To be added in future PR.

## Linting and Styling

To be added in future PR.

## FastAPI Resources

- [Documentation](https://fastapi.tiangolo.com/)
