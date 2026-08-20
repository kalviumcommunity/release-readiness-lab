# Use official lightweight Python image.
FROM python:3.11.9-slim

# Set working directory.
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependencies first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .

# Expose port
EXPOSE 5000

# Run Flask using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
