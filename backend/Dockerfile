FROM python:3.11-slim

RUN pip install uv

WORKDIR /app
COPY requirements.lock pyproject.toml README.md ./

RUN uv pip install --no-cache --system -r requirements.lock

EXPOSE 8000

COPY src .

CMD ["python", "debates.py", "serve"]
