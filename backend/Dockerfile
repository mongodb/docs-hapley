FROM python:3.10-bullseye
WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pip install pipenv \
    && pipenv install --system
COPY *.py ./
COPY ./api ./api
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
