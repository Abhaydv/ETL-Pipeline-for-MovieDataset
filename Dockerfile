FROM python:3.11-slim

WORKDIR /app

# Install system deps (if any) and copy project
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

# Make entrypoint executable and use it so migrations run at container start
RUN chmod +x /app/entrypoint.sh || true
ENTRYPOINT ["/app/entrypoint.sh"]
