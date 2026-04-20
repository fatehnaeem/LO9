# Student Tasks - Week 9 (Starter)

## Task 0 - Definition of Done
Add a short section to README with your success criteria:
- docker build succeeds
- docker compose up runs API + dependency
- /health returns 200
- /ready returns 200 when dependency is up and 503 when dependency is down
- CI pipeline runs on push and pull request

## Task 1 - Dockerfile for API
Create Dockerfile at project root.

Suggested content:

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

Verify:
- docker build -t week9-flask-api:dev .
- docker run --rm -p 5000:5000 week9-flask-api:dev
- curl -s http://localhost:5000/health

## Task 2 - Compose Stack (API + Redis)
Create docker-compose.yaml.

Minimum target:
- api service builds from current folder
- redis service uses image redis:7-alpine
- api receives REDIS_URL=redis://redis:6379
- api depends_on redis

Verify:
- docker compose up --build
- curl -s http://localhost:5000/health
- curl -i http://localhost:5000/ready

## Task 3 - Health, Readiness, Structured Logs
Update app.py:
1. /health endpoint
   - returns 200 and JSON status when process is alive.
2. /ready endpoint
   - use redis client ping
   - return 200 when ping succeeds
   - return 503 when ping fails
3. Structured logs
   - log one JSON line per request
   - include method, path, status, latencyMs, requestId

Failure demo:
- Start stack: docker compose up --build
- Stop redis: docker compose stop redis
- Check readiness: curl -i http://localhost:5000/ready
- Expected result: HTTP 503

## Task 4 - Minimal CI
Create .github/workflows/ci.yml with:
- trigger: push to main + pull_request
- setup python
- install dependencies
- run checks (minimum: python -m py_compile app.py)

Optional stronger checks:
- add pytest and run tests
- docker build in CI

## Recommended References
- Flask docs: https://flask.palletsprojects.com/
- Redis for Python: https://redis.readthedocs.io/en/stable/
- Docker Compose networking: https://docs.docker.com/compose/how-tos/networking/
- GitHub Actions Python template: https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-python
