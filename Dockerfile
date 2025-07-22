# Use official lightweight Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 8080

# Default environment variables
ENV PORT=8080

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:test_app"]

