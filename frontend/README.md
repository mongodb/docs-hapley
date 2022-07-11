<h1 align="center">
  Hapley Frontend
</h1>

## Local Development

### Non-Containerized Development

Once inside the `frontend` directory, run `npm install` to install all project dependencies.

Create a `.env.development` file with the same format as `.env.example`, but with values populated. `GATSBY_API_URL` should equal `http://localhost:8000/api/v1`. Please ensure you have the backend running locally by following the instructions in the backend [README](../backend/README.md)

Then run `npm run develop`. The site should now be running at `http://localhost:3000`.

To build and serve the site, run:

```shell
$ npm run build
$ npm run serve
```

You can read more about the Gatsby build process [here](https://www.gatsbyjs.com/docs/conceptual/overview-of-the-gatsby-build-process/).

### Containerized Development with Docker

To take advantage of Gatsby development features such as hot reloading, please use `npm run develop`. Although you can configure hot reloading with Docker development via volumes, we leverage Docker for our production environment. Therefore, you should only use Docker locally when attempting to replicate the production environment.

If you'd like to develop locally using Docker, first ensure that you have Docker installed on your machine. You can download and install Docker [here](https://docs.docker.com/get-docker/).

Once Docker is installed, run `npm run clean` to ensure you've removed `.cache` and `public` directories. Building an image without clearing the cache will result in a compilation error at the `npm run build` stage. You can launch the frontend two ways:

1. With `docker compose`: In the project root, you can run:

```
docker compose build
docker compose up
```

`docker compose` allows you to launch multiple services simultaneously (i.e. both `frontend` and `backend`).

TODO: conslidate Docker compose instructions once implemented for backend service

2. With `docker build` and `docker run`: In the `frontend` directory, you can run:

```
docker build -t hapleyfrontend ./
docker run -p 3000:3000/tcp hapleyfrontend:latest
```

## Testing

We leverage [Jest](https://jestjs.io/) and [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) to test our frontend code.

To run the entire test suite, run `npm run test`. For just unit tests, run `npm run test:unit`

Individual tests can be run directly with Jest. For example, `jest ./tests/unit/HelloWorld.test.tsx`

## Linting and Styling

We use [ESLint](https://eslint.org) and [Prettier](https://prettier.io) to help with linting and style. Both ESLint and Prettier run during the pre-commit hook to ensure pushed code maintains clean style and formatting.

Linting and formatting checks also run as part of CI via GitHub Actions to maintain a clean `main` branch.

To run the linter, use `npm run lint`. If you want to automatically fix issues detected by the linter, use `npm run lint:fix`. The analogous commands exist for Prettier, namely `npm run format` and `npm run format:fix`.

## Environment Variables

Gatsby has support for automatic loading of environment variables into the browser. In development, Gatsby looks for `.env.development`. Similarly, it looks for `.env.production` during builds.

To expose a non-secretive environment variable in the browser, preface its name with `GATSBY_`. To load environment variables into Node.js, follow instructions [here](https://www.gatsbyjs.com/docs/how-to/local-development/environment-variables/).

If you add a new environment variable, add it to the `.env.example` file for future reference. Also update the build args for the Docker image in our Drone pipeline. If the environment variable is a secret, add it to Drone's secret store. You can read more about secrets [here](https://docs.drone.io/secret/repository/).

## Gatsby Resources

- [Documentation](https://www.gatsbyjs.com/docs/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Tutorials](https://www.gatsbyjs.com/tutorial/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Guides](https://www.gatsbyjs.com/tutorial/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [API Reference](https://www.gatsbyjs.com/docs/api-reference/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Plugin Library](https://www.gatsbyjs.com/plugins?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)

- [Cheat Sheet](https://www.gatsbyjs.com/docs/cheat-sheet/?utm_source=starter&utm_medium=readme&utm_campaign=minimal-starter-ts)
