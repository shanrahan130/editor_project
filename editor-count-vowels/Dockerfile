FROM python:3.8-slim

WORKDIR /app

# Copy all files into the container
COPY . /app

# Install Flask
RUN pip install Flask

# Expose port 80
EXPOSE 80

# Run the app
CMD ["python", "app.py"]
