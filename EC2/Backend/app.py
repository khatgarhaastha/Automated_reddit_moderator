from flask import Flask, jsonify, request
from main import process_llama, generate_nsfw_flags  # Import your Lambda function code

app = Flask(__name__)

@app.route('/generate_nsfw_flags', methods=['POST'])
def generate_nsfw_flags():
    print("Request received", request.get_json())
    # Get 'limit' from the request body (if provided)
    data = request.get_json()
    limit = data.get('limit', None) if data else None

    # Call the Lambda function
    result = generate_nsfw_flags(limit)

    # Return the result as JSON
    return jsonify(result), result['statusCode']

@app.route('/process_using_llama', methods=['POST'])
def process_using_llama():
    print("Request received", request.get_json())
    # Get 'limit' from the request body (if provided)
    data = request.get_json()
    limit = data.get('limit', None) if data else None

    # Call the Lambda function
    result = process_llama(limit)

    # Return the result as JSON
    return jsonify(result), result['statusCode']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
