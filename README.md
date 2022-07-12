# Hapley

Hapley is an internal admin interface to manage aspects of the MongoDB documentation.

## Tech Stack

Hapley exposes a REST API on top of the Docs Atlas cluster using the [FastAPI framework](https://fastapi.tiangolo.com/). The frontend is written in [Gatsby](https://www.gatsbyjs.com/) with Typescript.

## Frontend

To read more about the application frontend, see the [README](./frontend/README.md) in the `frontend` directory.

## Backend

To read more about the application backend, see the [README](./backend/README.md) in the `backend` directory.

## Development and Deployment Workflow

Create a new branch off of `main` with your changes for a given feature or bug fix. Please include the JIRA ticket within the branch name. For example, `dop-1234-test`.

When you are ready to contribute your changes, open a pull request against `main` with the ticket name in the title. You should also link to the Jira ticket within the pull request description. Once a PR is opened, tests will be run via GitHub Actions. You can read more about the linting and testing tools we use in the READMEs for `backend` and `frontend`. All PRs must pass the pull request checks prior to merging. Additionally, you must receive at least one PR approval prior to merging. Pull requests gets squashed into a single commit upon merging into `main`.

### Staging Release 

Hapley is deployed on the Kanopy platform. A merge into `main` triggers the Drone pipelines setup in `.drone.yml`. Once the build is completed, it is promoted to staging automatically.

- Backend staging link: https://hapley.docs.staging.corp.mongodb.com/api/v1
- Frontend staging link: https://hapley.docs.staging.corp.mongodb.com/

### Production Release

TBD. Need to determine production release workflow once we've finished application development. Perhaps take inspiration from the [Dev Center setup](https://github.com/mongodb/devcenter#production-release).