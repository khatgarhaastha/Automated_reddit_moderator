
import boto3 
from transformers import pipeline
from boto3.dynamodb.conditions import Attr

# Fetch the items from DynamoDB table
def fetch_items_from_dynamodb(table_name, limit=None):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(table_name)
    filter_expression = Attr('label').not_exists() | Attr('label').eq('')

    if limit:
        response = table.scan(FilterExpression = filter_expression, Limit=limit)
    else:
        response = table.scan(FilterExpression = filter_expression)
    items = response['Items']
    return items

# Insert items into DynamoDB table
def insert_items_into_dynamodb(table_name, items):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table(table_name)
    for item in items:  
        table.put_item(Item=item)

# Function to parse text list as NSFW or SFW
def parse_nsfw_sfw(submissions):

    # Define the model from HuggingFace Transformers
    pipe = pipeline("text-classification", model="michellejieli/NSFW_text_classifier", truncation=True, max_length=512)

    for i,submission in enumerate(submissions):
        text = submission['submission_text']
        print(f'Processing submission Number :{i}\nText : {text}')
        if(text != None and len(text) > 0):
            prediction = pipe(text)[0]
            print(f'Prediction : {prediction}\n\n')
            submission['score'] = str(prediction['score'])
            submission['label'] = prediction['label']
        else:
            print(f'No text found for this submission')
    
    return submissions

# Lambda function handler
def lambda_handler(limit = None):
    
    submissions = fetch_items_from_dynamodb('reddit-submissions', limit)

    # Parse the submissions
    submissions = parse_nsfw_sfw(submissions)

    # Insert the items into DynamoDB table
    insert_items_into_dynamodb('reddit-submissions', submissions)

    return {
        'statusCode': 200,
        'body': 'NSFW/SFW classification completed!'
    }


