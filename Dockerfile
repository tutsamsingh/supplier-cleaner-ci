# Start from a small official Python image
FROM python:3.12-slim

# All app files go in /code inside the container
WORKDIR /code

# Install dependencies first (Docker caches this step if requirements.txt doesn't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app ./app

# Start the API on port 8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
