FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh .
COPY indexer.py .

ENTRYPOINT ["/app/wait-for-it.sh", "elasticsearch", "--", "python", "indexer.py"]
