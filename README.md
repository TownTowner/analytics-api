## Prepare:
`uv init` in thr root dir.

## local:
first:
- `cd src`

then:
- `uvicorn main:app --reload`
- `python -m uvicorn main:app --reload`

## Docker:
- `docker build -t analytics-api .`
- `docker run analytics-api`
 
## Docker compose
- `docker compose up --watch`
- `docker compose down` or `docker compose down -v`(remove volumes)
- `docker compose run app /bin/bash` or `docker compose run app python`