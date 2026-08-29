# CI/CD and GitHub Workflow Strategy

## Git Workflow vs CI/CD

Git and GitHub actions such as creating branches, committing, pushing, opening pull requests, merging, pulling `main`, and deleting branches are version-control and collaboration workflow.

Continuous Integration starts when GitHub Actions automatically validates changes after events such as `pull_request`, `push`, or manual `workflow_dispatch`. Continuous Delivery or Deployment starts when automation publishes, releases, or deploys after validation. This Selenium project currently has no deployment target, so CD is future scope.

## Recommended Branch Flow

Use short-lived feature branches for framework and test changes:

```powershell
git switch main
git pull origin main
git switch -c feature/<short-change-name>
```

Before opening a pull request:

- Run `.venv\Scripts\pytest` locally.
- Commit only intentional source and documentation changes.
- Do not commit `.env`, `.venv/`, reports, screenshots, caches, or generated runtime files.
- Push the branch and open a PR into `main`.

After merge:

```powershell
git switch main
git pull origin main
git branch -d feature/<short-change-name>
git push origin --delete feature/<short-change-name>
```

## GitHub Actions Strategy

No workflow YAML exists in this repository yet. When CI is added, keep it small and aligned with local commands.

Recommended jobs:

- `smoke`: run on pull requests; install Python dependencies and execute the fastest reliable Selenium pytest subset.
- `regression`: run on `main` pushes and manual dispatch; execute the full Chrome-only Selenium suite.

Recommended workflow behavior:

- Use `actions/checkout` to fetch the repository.
- Use `actions/setup-python` with pip caching based on `requirements.txt`.
- Install dependencies with `python -m pip install --upgrade pip` and `pip install -r requirements.txt`.
- Run pytest using the same command style used locally.
- Upload `reports/` and `screenshots/` as artifacts when present.

## Environment Variables and Secrets

Use workflow `env` values for non-sensitive configuration:

- `BASE_URL`
- `HEADLESS`
- `DEFAULT_TIMEOUT`
- `ACTION_DELAY`

Use GitHub Secrets only for sensitive values. Never store secrets in workflow YAML, `.env`, reports, screenshots, logs, or caches.

Set the default `GITHUB_TOKEN` permissions to least privilege, then increase permissions only for jobs that truly need them.

## Artifacts, Reports, and Debugging

CI should preserve test evidence without committing generated files:

- Upload `reports/report.html` for pytest-html results.
- Upload `screenshots/` for failure evidence.
- Keep artifacts short-lived unless longer retention is required for audit.
- Prefer headless CI runs; use headed or slow-motion runs locally for visual debugging.

Use dependency caching to speed up CI, but never cache paths containing secrets, tokens, `.env`, browser profiles, reports, or screenshots.

## Audit Checklist

Before accepting CI/CD changes, verify:

- Workflow triggers match the intended branch policy.
- Job names clearly describe purpose, such as `smoke` or `regression`.
- CI commands can be reproduced locally.
- Python and dependency installation are explicit.
- Environment variables are non-secret and documented.
- Secrets are read only from GitHub Secrets.
- `GITHUB_TOKEN` permissions follow least privilege.
- Reports and screenshots are uploaded as artifacts, not committed.
- Selenium remains Chrome-only unless broader browser coverage is explicitly requested.
- The sibling Playwright project is not modified.
