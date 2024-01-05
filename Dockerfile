FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    nano \
    vim \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --dev

COPY . .

CMD [ "/app/entrypoint.sh" ]
