# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
# Since 'main_analytic' contains 'manage.py', we copy its contents to '/app'
COPY main_analytic/ /app/

# Expose the port the app runs on
EXPOSE 8004

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8004"]
