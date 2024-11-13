# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY sim_registration/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the Django project into the container
COPY sim_registration /app

# Copy the .env file if needed
COPY sim_registration/.env /app/.env

# Expose the port your app runs on
EXPOSE 8000

# Collect static files (if using Django's collectstatic)
RUN python manage.py collectstatic --no-input

# Run the Django app with Gunicorn
CMD ["gunicorn", "sim_registration.wsgi:application", "--bind", "0.0.0.0:8000"]
