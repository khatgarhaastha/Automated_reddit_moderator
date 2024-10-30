FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install necessary Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
