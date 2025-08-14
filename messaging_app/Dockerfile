# Use official Python image as the base
FROM python:3.10-slim

# Set a working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file(s) and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code
COPY . .

# Expose the port the app runs on (default is 8000 for Django/FastAPI)
EXPOSE 8000

# Define how to start the app
# For Django:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# For FastAPI (if main.py with FastAPI instance named app):
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 
