# Base image
FROM python:3.11-slim

# Prevent .pyc and buffer issues
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run server using Gunicorn (production-ready)
CMD ["gunicorn", "venkat_project.wsgi:application", "--bind", "0.0.0.0:8000"]
