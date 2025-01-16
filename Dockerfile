FROM python:3.12-slim

# Install PostgreSQL development libraries
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential

# Set working directory
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the start script executable
RUN chmod +x scripts/start.sh

# Expose the application port
EXPOSE 8000

# Command to run the app
CMD ["scripts/start.sh"]