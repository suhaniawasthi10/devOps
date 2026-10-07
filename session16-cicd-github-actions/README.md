# Session 16 — Calculator CI/CD

**Suhani Awasthi · 24BCS10260**

A small HTTP calculator implements addition, subtraction, multiplication and division with bounded numeric input and error handling. Tests cover arithmetic, invalid types, division by zero and HTTP responses. This is an original equivalent of the reference calculator project; the teacher's exact `10-final-cicd-pipeline` source was not provided.

From this folder: create a Python 3.13 virtual environment, `pip install -r requirements-dev.txt`, `python -m pytest -q`, then `bash build.sh`. Run the service with `gunicorn --bind 127.0.0.1:8081 app.calculator:app`. POST `{"operation":"add","a":3,"b":4}` to `/calculate` with Content-Type application/json; expect result 7.

The active workflow lives at [repository-root .github/workflows/ci.yml](../.github/workflows/ci.yml). CI installs dependencies, tests and packages an artifact. Delivery builds a Docker image, deploys it into an isolated container on the runner and verifies its HTTP behavior. This is a disposable demonstration deployment; it does not claim to host a permanent production endpoint. The later [DevSecOps pipeline](../.github/workflows/devsecops.yml) adds registry publication and Kubernetes deployment.

| Concept | Implementation |
|---|---|
| Workflow | YAML triggered on matching pushes/PRs and manual dispatch |
| Job | test-build-deliver executes on an ubuntu-latest runner |
| Steps | Checkout → Python setup → tests → build → artifact → container → smoke test |
| Runner | Temporary machine provided by GitHub Actions |
| Secrets | Optional DEMO_SECRET via environment, presence checked without printing value |
| Artifacts | Calculator tarball, build metadata and JUnit results |
| CI | Automatically checks integration before a release candidate is accepted |
| CD | Delivers and verifies a runnable candidate after successful checks |

Later: push this work, enable Actions, run the workflow, retain the run URL and screenshot each job. To demonstrate failure, temporarily change addition to return an incorrect result on a branch, observe failing tests, restore it and capture the passing run. Do not submit the intentionally broken application.
