FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 8000

# Add bulk log generator
COPY generate_bulk_logs_docker.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]