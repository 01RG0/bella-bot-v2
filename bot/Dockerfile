FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --upgrade pip && pip install -e .

COPY . .

CMD ["python", "-m", "bella_bot"]