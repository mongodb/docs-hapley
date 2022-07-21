# Hapley

Hapley is an internal admin interface to manage aspects of the MongoDB documentation.

## Tech Stack

Hapley exposes a REST API on top of the Docs Atlas cluster using the [FastAPI framework](https://fastapi.tiangolo.com/). The frontend is written in [Gatsby](https://www.gatsbyjs.com/) with Typescript. Hapley is deployed to Kanopy via a series of Drone pipelines.

## Frontend

To read more about the application frontend, see the [README](./frontend/README.md) in the `frontend` directory.

## Backend

To read more about the application backend, see the [README](./backend/README.md) in the `backend` directory.

## Environment Variables

Environment variables used are declared in the values file for each environment stored in the `environments` folder at the project root. Non-secretive environment variables can be added directly as keys under the `env` parameter. Secrets must be referenced under the `envSecrets` parameter. You can read more about configuring the web-app Helm chart [here](https://github.com/10gen/helm-charts/tree/master/charts/web-app).

### Secrets

> Note: You must be connected to VPN to access these resources.

First ensure you've installed and configured `kubectl` according to [these instructions](https://github.com/10gen/kanopy-docs/blob/master/docs/configuration/kubeconfig.md). Hapley lives under the `docs` namespace. To add secrets to the staging environment, ensure that your current context is `"api.staging.corp.mongodb.com"`. For prod, use `"api.prod.corp.mongodb.com"`.

[This doc](https://github.com/10gen/kanopy-docs/blob/master/docs/configuration/helm.md) contains information on the `ksec` plugin, which is used to managed Kubernetes secrets. To get the Hapley secrets for your current context, run `helm ksec get docs-hapley`. To add a new secret for the current context, run `helm ksec set mysecret variable1=value1`. You then need to add a reference to that secret with the value file in the `environments` folder.


> Note: Secrets referenced in Drone pipelines are sourced from the [repo secrets accessible via the Drone UI](https://docs.drone.io/secret/repository/).

**AWS Parameter Store**:

Although we store application secrets in k8s, we leverage AWS Param Store to share long term secrets. You can find the values in AWS Param Store [here](https://us-east-2.console.aws.amazon.com/systems-manager/parameters/?region=us-east-2&tab=Table#list_parameter_filters=Name:Contains:hapley). If you add a new secret to k8s or Drone, add it to param store as well for team visibility and to maintain a single source of truth.

**Kanopy Portal**:

All k8s secrets for the `docs` namespace can be accessed via the Kanopy portal. The staging portal is [here](https://kanopy.staging.corp.mongodb.com/docs/secrets/docs-hapley), and the production portal is [here](https://kanopy.prod.corp.mongodb.com/docs/secrets/docs-hapley).

## Development and Deployment Workflow

### Pre-commit Hooks

This monorepo uses [pre-commit](https://github.com/pre-commit/pre-commit) to
help lint and format both backend and frontend files before they are committed
through git.

With python 3.10, install and set up `pre-commit` for this repo by doing the
following:

```
pip install pre-commit
pre-commit install
```

This will allow `pre-commit` to be run when doing `git commit`. To test pre-commit
hooks locally, run:

```
pre-commit run
```

### Pull Requests

Create a new branch off of `main` with your changes for a given feature or bug fix. Please include the JIRA ticket within the branch name. For example, `dop-1234-test`.

When you are ready to contribute your changes, open a pull request against `main` with the ticket name in the title. You should also link to the Jira ticket within the pull request description. Once a PR is opened, tests will be run via GitHub Actions. You can read more about the linting and testing tools we use in the READMEs for `backend` and `frontend`. All PRs must pass the pull request checks prior to merging. Additionally, you must receive at least one PR approval prior to merging. Pull requests gets squashed into a single commit upon merging into `main`.

### Staging Release

Hapley is deployed on the Kanopy platform. A merge into `main` triggers the Drone pipelines setup in `.drone.yml`. Once the build is completed, it is promoted to staging automatically.

- Backend staging link: https://hapley.docs.staging.corp.mongodb.com/api/v1
- Frontend staging link: https://hapley.docs.staging.corp.mongodb.com/

### Production Release

TBD. Need to determine production release workflow once we've finished application development. Perhaps take inspiration from the [Dev Center setup](https://github.com/mongodb/devcenter#production-release).

## Resources
- [Kanopy Tutorial](https://github.com/10gen/kanopy-docs/blob/master/docs/getting_started/README.md)
