# Use a small, official Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

EXPOSE 8080

# Run with waitress (production-ready WSGI server) instead of Flask's dev server
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8080", "wsgi:app"]
