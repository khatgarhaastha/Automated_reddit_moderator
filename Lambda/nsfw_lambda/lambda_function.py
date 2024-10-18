
import boto3 
from transformers import pipeline

# Fetch the items from DynamoDB table
def fetch_items_from_dynamodb(table_name, limit=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    if limit:
        response = table.scan(Limit=limit)
    else:
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

    # Define the model from HuggingFace Transformers
    pipe = pipeline("text-classification", model="michellejieli/NSFW_text_classifier")

    for submission in submissions:
        text = submission['submission_text']
        prediction = pipe(text)[0]
        prediction['score'] = str(prediction['score'])
        submission['nsfw_tags'] = prediction
    
    return submissions

# Lambda function handler
def lambda_handler(event, context):
    limit = None

    # Fetch the items from DynamoDB table
    if 'limit' in event:
        limit = event['limit']
    
    submissions = fetch_items_from_dynamodb('reddit-submissions', limit)

    # Parse the submissions
    submissions = parse_nsfw_sfw(submissions)

    # Insert the items into DynamoDB table
    insert_items_into_dynamodb('reddit-submissions', submissions)

    return {
        'statusCode': 200,
        'body': 'NSFW/SFW classification completed!'
    }


