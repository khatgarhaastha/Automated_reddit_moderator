FROM amazon/aws-lambda-python:3.9


RUN pip3 install torch
# Install dependencies
RUN pip install --no-cache-dir boto3 botocore transformers

# Copy your lambda function script into the container
COPY lambda_function.py ./

# Set the CMD to your handler (filename.function)
CMD ["lambda_function.lambda_handler"]