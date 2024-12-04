FROM python:3.8-slim

WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install Flask requests

# Expose port 80 (if needed)
EXPOSE 80

# Run the monitoring script
CMD ["python", "monitoring.py"]
