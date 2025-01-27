# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install system dependencies required for PostgreSQL
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the Python dependencies from the requirements.txt file
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Expose the port that the app will run on
EXPOSE 8000

# Make migrations and collect static files (optional)
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Start the application using gunicorn (or any other WSGI server you prefer)
CMD ["gunicorn", "yourproject.wsgi:application", "--bind", "0.0.0.0:8000"]
