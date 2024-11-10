# Use --platform=linux/amd64 to force compatibility on Apple Silicon Macs
FROM --platform=linux/amd64 amazon/aws-lambda-python:3.9

# Install dependencies
RUN pip install --no-cache-dir boto3 botocore praw

# Copy your lambda function script into the container
COPY . .

# Set the CMD to your handler (filename.function)
CMD ["lambda_function.lambda_handler"]
