
# Lighter Dockerfile for better upload success
FROM python:3.9-slim

# Still vulnerable but smaller
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
RUN touch users.db && chmod 666 users.db

# Keep the vulnerabilities but reduce size
ENV SECRET_KEY="super-secret-key-123"
EXPOSE 5000

CMD ["python", "app.py"]