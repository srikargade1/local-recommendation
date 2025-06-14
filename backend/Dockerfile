# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Set environment variable to avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Gunicorn will run the Flask app defined in `app.py`
# Replace `app:app` if your entry point is different
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
