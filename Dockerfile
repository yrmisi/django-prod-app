FROM python:3.13.2-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip --no-cache-dir \
    && pip install --no-cache-dir -r requirements.txt

COPY ./my_site /app/

CMD ["gunicorn", "my_site.wsgi:application", "--bind", "0.0.0.0:8000"]
