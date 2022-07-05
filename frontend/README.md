<h1 align="center">
  Hapley Frontend
</h1>

## Local Development

### Non-Containerized Development

Once inside the `frontend` directory, run `npm run develop`. The site should now be running at `http://localhost:8000`.

To build and serve the site, run:

```shell
$ npm run build
$ npm run serve
```

### Containerized Development with Docker

If you'd like to develop locally using Docker, ensure that you have Docker installed on your machine. You can download and install Docker [here](https://docs.docker.com/get-docker/).

Once Docker is installed, you can launch the frontend two ways:

1. With `docker build` and `docker run`: In the `frontend` directory, you can run:

```
docker build -f Dockerfile.dev -t hapleyfrontend ./
docker run -p 8000:8000/tcp -v $PWD/src:/app/src hapleyfrontend:latest
```

2. With `docker compose`: In the project root, you can run:

```
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up
```

`docker compose` allows you to launch multiple services simultaneously (i.e. both `frontend` and `backend`).

## Testing

We leverage [Jest](https://jestjs.io/) and [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) to test our frontend code.

To run the entire test suite, run `npm run test`. For just unit tests, run `npm run test:unit`

Individual tests can be run directly with Jest. For example, `jest ./tests/unit/HelloWorld.test.tsx`

## Linting and Styling

We use [ESLint](https://eslint.org) and [Prettier](https://prettier.io) to help with linting and style. Both ESLint and Prettier run during the pre-commit hook to ensure pushed code maintains clean style and formatting.

Linting and formatting checks also run as part of CI via GitHub Actions to maintain a clean `main` branch.

To run the linter, use `npm run lint`. If you want to automatically fix issues detected by the linter, use `npm run lint:fix`. The analogous commands exist for Prettier, namely `npm run format` and `npm run format:fix`.

## Gatsby Resources

- [Documentation](https://www.gatsbyjs.com/docs/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Tutorials](https://www.gatsbyjs.com/tutorial/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Guides](https://www.gatsbyjs.com/tutorial/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [API Reference](https://www.gatsbyjs.com/docs/api-reference/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Plugin Library](https://www.gatsbyjs.com/plugins?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Cheat Sheet](https://www.gatsbyjs.com/docs/cheat-sheet/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)
