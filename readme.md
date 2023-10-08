# FastAPI htmx server

## Quickstart (development mode)

You can either start up using `docker-compose`:

```sh
make build-dev
```

Or you can install from source:

```python
pip install -r ./build/requirements.txt
uvicorn app.main:app --reload
```
