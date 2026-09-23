# Hosted CI Policy

GitHub Actions / GitHub-hosted CI is intentionally disabled for this repository by owner decision. Do not add, require, re-enable, rerun, or depend on GitHub-hosted workflows for validation, merge readiness, deployment, or release acceptance.

Use local repository checks, deterministic tests, controlled disposable environments, and manual PR evidence instead. A PR is not blocked merely because no hosted GitHub Actions result exists; report the exact checks that actually ran.

Do not deploy through GitHub Actions and do not store production deployment secrets for Actions.

Red lines:
- no `.github/workflows/**` hosted-runner jobs;
- no hosted CI status requirement;
- no automatic production deployment from push/merge;
- no weakening local/runtime assertions because hosted CI is absent.

Any future CI automation requires a new explicit owner decision and must not assume GitHub-hosted paid runners.