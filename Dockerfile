FROM python:3.11-slim

RUN pip install uv

WORKDIR /app
COPY requirements.lock pyproject.toml ./

RUN uv pip install --no-cache --system -r requirements.lock

COPY src .
CMD ["python", "debates.py", "--help"]
