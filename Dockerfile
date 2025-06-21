# Use an official Python 3.11 image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

RUN mkdir -p /app/media

# Expose port (default for gunicorn)
EXPOSE 8000

# Start the app with Gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py create_admin && gunicorn LTResultManager.wsgi"]
