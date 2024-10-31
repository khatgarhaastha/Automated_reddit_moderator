from flask import Flask, jsonify, request
from nsfw_filter import lambda_handler  # Import your Lambda function code

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    # Get 'limit' from the request body (if provided)
    data = request.get_json()
    limit = data.get('limit', None) if data else None

    # Call the Lambda function
    result = lambda_handler(limit)

    # Return the result as JSON
    return jsonify(result), result['statusCode']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
