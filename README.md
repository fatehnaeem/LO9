# Week 9 Flask DevOps Lab - Starter Project

## Goal
This project is your starting point for Week 9 laboratory tasks:
- Task 1: containerize API with Dockerfile
- Task 2: run API + dependency with Docker Compose
- Task 3: add health/readiness and structured JSON logs
- Task 4: add minimal CI workflow

The app already includes a small Flask API and a local SQLite database (`app.db`).

## Definition of Done
Success criteria for completing all tasks:
- ✓ `docker build -t week9-flask-api:dev .` succeeds
- ✓ `docker compose up --build` runs API + Redis without errors
- ✓ `curl http://localhost:5000/health` returns 200
- ✓ `curl http://localhost:5000/ready` returns 200 when Redis is up and 503 when Redis is down
- ✓ CI pipeline runs on push and pull request to main branch

## Local Run (without Docker)
1. Open terminal in this folder.
2. Create virtual environment and install dependencies:

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Start app:

   python app.py

4. Test endpoints:

   curl -s http://localhost:5000/
   curl -s http://localhost:5000/ping
   curl -s http://localhost:5000/notes

## What Students Must Modify/Add
See [STUDENT_TASKS.md](STUDENT_TASKS.md) for exact steps.

In short, students should:
1. Add Dockerfile at project root.
2. Add docker-compose.yaml with services:
   - api (this app)
   - redis (for readiness checks)
3. Update app.py:
   - /health returns 200 when process is alive
   - /ready checks Redis availability and returns 200 or 503
   - each request logs JSON with method/path/status/latency/requestId
4. Add GitHub Actions workflow in .github/workflows/ci.yml.

## Suggested File Targets for Tasks
- app.py
- Dockerfile (new)
- docker-compose.yaml (new)
- .github/workflows/ci.yml (new)
- README.md (add demo results)

## Useful References
- Flask docs: https://flask.palletsprojects.com/
- Flask request hooks: https://flask.palletsprojects.com/en/stable/api/#flask.Flask.before_request
- Redis Python client: https://redis.readthedocs.io/en/stable/
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker Compose file reference: https://docs.docker.com/compose/compose-file/
- GitHub Actions quickstart: https://docs.github.com/actions/quickstart
- HTTP 503 semantics: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/503
- Structured logging (JSON): https://betterstack.com/community/guides/logging/structured-logging/
