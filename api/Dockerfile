FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./prestart.sh /app/prestart.sh
COPY ./requirements/prod.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/