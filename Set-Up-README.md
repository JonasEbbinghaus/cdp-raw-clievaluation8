# cdp_raw_clievaluation8

> One-line description of this data product (purpose + scope).

---

## Overview
- **Product name:** `cdp_raw_clievaluation8`
- **Layer:** `raw`
- **Domain:** `Not provided`

- **Owner / Team:** `{{TEAM_NAME}}`

- **contact**: jonas.ebbinghaus@vaillant-group.com

- **Status:** `{{status: draft / experimental / production}}`
- **Version:** `{{semver or date}}`

- **Repository created by:** CLI tool (asset bundle included, pushed to `dev` branch)
- **Workspaces created / configured:** Dev workspace (isolated Unity Catalog) and Prod workspace (shared metastore)

This repository is a scaffolded starting point created by a CLI that bootstraps a data product and its asset bundle. It is intentionally opinionated with CI/CD best-practices and a template Data Contract so teams can start developing quickly while keeping governance and operational controls in place.

---

## What the CLI created for you (automatically)
The CLI that ran to create this repo performed the following actions for the given `cdp_raw_clievaluation8` and `raw`:

- Created a GitHub repository with two branches:
  - `dev` — initial code and asset bundle pushed here
  - `main` — protected branch (no direct pushes; go via PR)
- Initialized a Databricks Asset Bundle in the repo and personalized bundle metadata (jobs, pipelines, targets, variables).
- Created Blob Containers (in the collaborative platform storage accounts) for both Dev and Prod. The specific storage account is determined by the chosen **layer**.
- Created **External Locations** in Dev and Prod that point to the corresponding Blob Containers.
- Configured Unity Catalog entries:
  - Dev workspace: isolated Unity Catalog tied to the Dev metastore, using the Dev external location.
  - Prod workspace: (shared) Unity Catalog or shared metastore, with the Prod external location.
- Created an **Account level group** with read access for consumers: `cdp-raw-cdp_raw_clievaluation8-readers`. This group is intended to be the standard consumer group for granting read access to the product in UC.
- Created the initial **Data Contract** file (see section below) and included it in the dev branch — the team must complete the contract fields.
- Added three starter GitHub Actions workflows (CI, deploy_dev, deploy_prod) in `.github/workflows/` tuned for Asset Bundles and Unity Catalog targets.
  - `ci.yml` — linting, dependencies, `databricks bundle validate`, contract tests
  - `deploy_dev.yml` — validate, deploy to Dev, run smoke test, upload logs
  - `deploy_prod.yml` — validate, check external location, deploy to Prod (requires environment approval)

Please delete this section and add documentation as in `Quickstart — what to do now (developers / operators)` step 3!

---

## Quickstart — what to do now (developers / operators)

1. Fill this README: replace placeholders `{{...}}` with real values (team, contact, status, etc.).

2. Create GitHub Environments and secrets (see *CI/CD* section below).
3. Customize this README.md and delete sections that do not apply to your data product.
   README Checklist for Data Products:s
   - Project Title – Clear and descriptive name of the data product
   - Short Description – What does the product do? What is its purpose?
   - Responsible Contacts – Who owns the product (business & technical)?
   - Data Sources – Where does the data come from? Internal/external?
   - Included Assets – List of datasets, pipelines, dashboards, etc.
   - Usage & Consumers – Who uses it and how (API, dashboard, etc.)
   - Technical Stack – Tools, platforms, languages used
   - Quality Assurance – Validation rules, tests, monitoring
   - Related Documentation – Links to Confluence, tickets, wiki, etc.
     - Link the data contract!
4. Work on feature branches off `dev`. Open PRs to `main` to promote to production with the required approvals. Adapt the asset bundle to your project!

Don't forget to adjust the data contract!!

---

## Data Contract (template)
The initial Data Contract file `<product-name>/datacontract.yaml` has been created in the repository, but must be completed by the product owner before the product is used in production.
The contract follows the **[Data Contract Specification 1.2.0](https://datacontract.com/)** and will be validated in the CI/CD process.

### Data Contract — required fields
- **`id`** *(Required)* — unique technical name of the data product (e.g., cdp_raw_clievaluation8). Was set automatically!
- **`info.title`** *(Required)* — human-readable title of the data product.
- **`info.version`** *(Required)* — version number of the data contract (not the data itself). Was set automatically!
- **`info.description`** *(Required)* — short and clear description, including primary use cases.
- **`info.owner`** *(Required)* — role or function responsible (e.g., “Salesforce Data Steward”).
- **`info.contact`** *(Required)* — name and contact details (email, Slack, etc.) of the owner.
- **`servers.development` / `servers.production`** *(Required)* — connection details to the Databricks workspace, including host, catalog, and schema.
- **`terms`** *(Required)* — usage terms, limitations, billing information, notice period.
- **`models`** *(Required)* — all tables/views including:
  - Description
  - Fields with `type`, `description`, required attributes (`required`), primary key (`primaryKey`), and optional `format`
  - Optional `quality` checks (SQL, rules, thresholds)
  - Example data (`examples`)
- **`servicelevels`** *(Required)* — availability, retention period, freshness threshold (including `timestampField`), and update frequency.
- **PII / GDPR** *(Required if applicable)* — indicate whether sensitive data is present and how it is handled.
- **Access & Consumer Group** *(Required)* — group in the format cdp-raw-cdp_raw_clievaluation8-readers, description of how to request access.

💡 Add any additional fields your organization requires (e.g., cost center, sensitivity label, regulatory notes).

---

## CI/CD — How workflows are wired and what you must configure

### Secrets & GitHub Environments (required)
Create two GitHub Environments and add the following secrets (names used in the workflows shipped in `.github/workflows/`):

1. `databricks-dev` environment (name suggestion):
   - `DATABRICKS_HOST_DEV` — Dev workspace host URL (e.g. `https://adb-<id>.azuredatabricks.net`)
   - `DATABRICKS_TOKEN_DEV` — token / service principal token for CI (dev identity)

2. `production` environment:
   - `DATABRICKS_HOST_PROD`
   - `DATABRICKS_TOKEN_PROD`

**Notes:**
- The Dev Unity Catalog is *workspace-isolated*.

### What each workflow does (high level)
- **CI (`ci.yml`)**: runs on pushes to `dev` and PRs to `main`. Linting, formatting checks, dependency install, `databricks bundle validate --target dev`, and local data contract test. This step protects `main` by ensuring basic quality before merges.
- **Dev deploy (`deploy_dev.yml`)**: runs on pushes to `dev`. Validates the bundle and data contract, checks the external location, deploys the bundle to Dev workspace, runs a smoke job, uploads logs.
- **Prod deploy (`deploy_prod.yml`)**: runs on merges to `main`. Validates the bundle and data contract, checks the external location, deploys bundle to Prod using `DATABRICKS_TOKEN_PROD`. This workflow should be protected by requiring manual approval in the `production` GitHub Environment.

### Best-practice knobs included in the workflows
- `fetch-depth: 0` on checkout (preserves Git metadata some bundles use)
- `databricks bundle validate` before `deploy`
- Testing the data contract via the CLI `datacontract test /path/to/datacontract.yaml`
- `databricks bundle deploy --auto-approve` to run non-interactively in CI (be careful with destructive ops)
- smoke tests executed via `databricks bundle run --job ...` and logs uploaded as workflow artifacts

---

## Tests & where to add them
Keep these test types in the `tests/` folder:

- **Smoke tests** (`tests/smoke/`) — quick checks run in Dev after deploy. Add a `tests/smoke/test_smoke.py` that uses small fixtures and a short runtime.
- **Unit tests** (`tests/unit/`) — logic-level tests for transformation code.
- **Integration tests** (`tests/integration/`) — larger transforms, maybe with small sample datasets or local Spark in Docker.
- **Acceptance tests** (`tests/acceptance/`) — consumer-facing validations run as part of release gating (optionally on Prod).

Make sure tests are runnable by `pytest` and documented at the top of each test file. The `CI` job runs `pytest` for contract tests by default.

Adapt this section to the test you have created for your data product (e.g., test procedures, test types, or a description of what is being tested)!

---

## Permissions & governance (short)
- Group created: `cdp-raw-clievaluation8-readers` — add consumers here to grant read access to UC objects for this product.

Please delete this section and add documentation as in `Quickstart — what to do now (developers / operators)` step 3!

---

## Further documentation

Add further documentation about your data product here and provide additional links so that others can better understand your data product.

---

## Troubleshooting
- **Bundle validate errors**: run `databricks bundle validate --target dev` locally and inspect the failing resource. The CI `ci.yml` also runs this on PRs to `main`.
- **Failed smoke test**: download `smoke_run.log` from the workflow artifact and inspect for errors. Check job definitions and parameterization under `resources/jobs/`.

---

## Template checklist (fill these now)

- [ ] Replace `{{TEAM_NAME}}`, `{{EMAIL_OR_SLACK}}`, `{{status}}`, `{{semver or date}}`

- [ ] Create GitHub Environments `databricks-dev` and `production` and add required host + token secrets
- [ ] Confirm that `cdp-raw-clievaluation8-readers` group exists and members know how to request access
- [ ] Pin action versions in `.github/workflows` (replace `@v1` / `@v4` with specific tags/sha you trust)
- [ ] Please adapt this README.md to your own data product after setting up the project (as described in step 3 in the section `Quickstart — what to do now (developers / operators)`).

---

## Where to get help
- Contact: jonas.ebbinghaus@vaillant-group.com

---