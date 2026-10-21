# supplier-cleaner-ci

A small FastAPI service that cleans messy supplier records (names, emails, prices, dates) and saves them to Postgres. The point of the project is its CI/CD pipeline, built with GitHub Actions and Docker.

## What the pipeline does

| Event | What runs |
|---|---|
| Pull request into `main` | Starts a Postgres container and runs all tests |
| Push / merge to `main` | Runs the tests, then builds the Docker image and pushes it to GitHub Container Registry |

Branch protection on `main` blocks merging any pull request whose tests fail.

## Run it locally

```bash
docker compose up --build
```

Then open http://localhost:8000/docs to try the API.

Example request to `POST /clean`:

```json
{ "name": "  acme   ROCKET co ", "email": " Sales@ACME.com ", "price": "$1,200.50", "date": "10/20/2026" }
```

Response:

```json
{ "name": "Acme Rocket Co", "email": "sales@acme.com", "price": 1200.5, "date": "2026-10-20" }
```

## Run the tests locally

```bash
docker compose up -d db
pip install -r requirements.txt
pytest -v
```

## Project layout

```
app/cleaner.py              cleaning logic (no web or database code)
app/main.py                 FastAPI endpoints + Postgres
tests/                      unit tests and API tests
Dockerfile                  builds the API image
docker-compose.yml          runs the API and Postgres together
.github/workflows/ci.yml    the CI/CD pipeline
```
