FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY . .

EXPOSE 8000

CMD ["/start"]