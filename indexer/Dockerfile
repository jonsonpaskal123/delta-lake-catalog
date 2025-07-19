FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh .
COPY indexer.py .

ENTRYPOINT ["/app/wait-for-it.sh", "elasticsearch"]
CMD ["python", "indexer.py"]
