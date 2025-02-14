FROM python:3.13.2-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==2.0.1"

RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml /app/

RUN poetry install --only main --no-interaction --no-root

COPY ./my_site /app/

# CMD ["gunicorn", "my_site.wsgi:application", "--bind", "0.0.0.0:8000"]
