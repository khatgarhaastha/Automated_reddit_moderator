import json 
import boto3
from config import * 
import asyncio
import requests 

# Fetch the list of subreddits from the S3. 


# for each subreddit : 
    # fetch data from specific subreddits - posts in the last 24 hours
    # Clean the posts -> make into a dictionary 
    # Store the posts in DynamoDB -> with 2 additional tags -> processed_nsfw = False, processed_rules = False

    # 2 calls in parallel 
        # 1. NSFW classification -> if NSFW -> processed_nsfw = True
        # 2. Rule classification -> processed_rules = True

    # Store the data back in DynamoDB

async def process_data():
        
        rule_processing_lambda_name = rule_lambda_function_name
        nsfw_processing_url = nsfw_processing_url
        
        rule_lambda_client = boto3.client('lambda')

        task1 = asyncio.create_task(requests.post(nsfw_processing_url, json={}))
        
        task2 = asyncio.create_task( rule_lambda_response = rule_lambda_client.invoke(
            FunctionName=rule_processing_lambda_name,
            InvocationType='Event',
            Payload=json.dumps({})
        )
    )

        await task1
        await task2

        

def lambda_handler(event, context):

    try:
        # Call the fetch and store Lambda function
        lambda_function_name = fetch_lambda_function_name
        fetch_lambda_client = boto3.client('lambda')
        fetch_lambda_response = fetch_lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps({})
        )

        if(fetch_lambda_response['StatusCode'] != 200):
            raise Exception('Error occurred while fetching the data!')

        # async 2 calls to NSFW and Rule classification Lambda functions
        
        asyncio.run(process_data())
        

        
        return {
            'statusCode': 200,
            'body': 'Data fetched and stored successfully!'
        }
    
    except Exception as e:
        
        return {
            'statusCode': 500,
            'body': e
        }
    