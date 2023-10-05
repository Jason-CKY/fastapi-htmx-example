FROM python:3.10 as dev

WORKDIR /app

COPY ./build/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


COPY ./app /app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

FROM dev as production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
