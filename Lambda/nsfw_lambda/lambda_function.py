
import boto3 
from transformers import pipeline

# Fetch the items from DynamoDB table
def fetch_items_from_dynamodb(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response['Items']
    return items

# Insert items into DynamoDB table
def insert_items_into_dynamodb(table_name, items):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    for item in items:
        table.put_item(Item=item)

# Function to parse text list as NSFW or SFW
def parse_nsfw_sfw(submissions):

    result = []

    # Define the model from HuggingFace Transformers
    pipe = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")

    for submission in submissions:
        text = submission['submissiontext']
        prediction = pipe(text)
        submission['nsfw_tags'] = prediction
    
    return submissions

# Lambda function handler
def lambda_handler(event, context):

    # Fetch the items from DynamoDB table
    submissions = fetch_items_from_dynamodb('Submissions')

    # Parse the submissions
    submissions = parse_nsfw_sfw(submissions)

    # Insert the items into DynamoDB table
    insert_items_into_dynamodb('Submissions', submissions)

    return {
        'statusCode': 200,
        'body': 'NSFW/SFW classification completed!'
    }


