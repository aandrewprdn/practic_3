FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry --no-cache

WORKDIR /code

RUN poetry config virtualenvs.create false


COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-dev

COPY . .

EXPOSE 3000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]