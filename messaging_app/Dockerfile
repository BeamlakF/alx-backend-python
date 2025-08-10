# Use official Python 3.10 base image
FROM python:3.10

# Set work directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into container
COPY . /app/

# Expose port 8000 (default Django port)
EXPOSE 8000

# Run Django development server (adjust if you use gunicorn or another server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
