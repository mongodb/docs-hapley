<h1 align="center">
  Hapley Frontend
</h1>

## Local Development

Once inside the `frontend` directory, run `npm run develop`. The site should now be running at `http://localhost:8000`.

To build and serve the site, run:

```shell
$ npm run build
$ npm run serve
```

Instructions on running via Docker are forthcoming.

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
