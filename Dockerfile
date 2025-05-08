# Use the official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 8080

# Set environment variable for Flask
ENV PORT=8080

# Command to run the app using Gunicorn (production-ready server)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
