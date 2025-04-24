
FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc g++ git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY tests ./tests
ENV PYTHONPATH=/app/src

CMD ["pytest", "-q"]
