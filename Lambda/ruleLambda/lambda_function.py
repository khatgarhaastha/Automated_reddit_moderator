
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from jinja2 import Environment, FileSystemLoader
import requests
from config import * 


def prepare_prompt(submissions, rules):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('prompt.j2')
    prompt = template.render(texts=submissions, rules=rules)
    return prompt


def fetch_items_from_dynamodb(table_name, limit=None):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    filter_expression = Attr("processed_rules").eq(False)

    table = dynamodb.Table(table_name)
    if limit:
        response = table.scan(FilterExpression=filter_expression,Limit=limit)
    else:
        response = table.scan(FilterExpression=filter_expression)
    items = response['Items']
    return items

def fetch_rules_from_dynamodb(table_name, limit=None):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

    table = dynamodb.Table(table_name)
    if limit:
        response = table.scan(Limit=limit)
    else:
        response = table.scan()
    items = response['Items']
    return items

def lambda_handler(event, context):
    # Fetch items from DynamoDB table
    submissions = fetch_items_from_dynamodb('reddit-submissions')

    # Fetch rules from DynamoDB table
    rules = fetch_rules_from_dynamodb('reddit-subreddit-rules')

    # Clean the rules and make a dictionary of subreddit and rules

    rule_dict = {}

    for rule in rules:
        subreddit = rule['subreddit']
        rule_text = rule['rules']
        rule_dict[subreddit] = rule_text
    
    # Create a submission dictionary 
        
    submission_dict = {}

    for submission in submissions:
        subreddit = submission['subreddit']
        submission_text = submission['submission_text']
        submission_id = submission['submission_id']
        if subreddit in submission_dict:
            submission_dict[subreddit].append({submission_id: submission_text}) 
        else:
            submission_dict[subreddit] = [{submission_id: submission_text}]

    # For each subreddit in the submission dictionary

    for subreddit in submission_dict:
        
        # Get the rules for the subreddit
        subreddit_rules = rule_dict[subreddit]
        
        
        # Get the submissions for the subreddit
        submissions = submission_dict[subreddit]

        print(f'Subreddit Name : {subreddit} \n Subreddit Rules : {subreddit_rules} \n Subreddit Submission Length : {len(submissions)}')
        
        # Batch the submissions into lists of 50

        for i in range(0, len(submissions), 1):
            
            # For each batch
            batch = submissions[i:i+1]
            prompt = prepare_prompt(batch, subreddit_rules)
            print(len(prompt))
            # Call the EC2 Ollama Llama model -> get the output
            
            payload = {
            "prompt": prompt,
            "model" : "llama3.2",
            "stream":False
            }

            #print(payload)
            results = requests.post(url = ollama_ec2_url , json=payload).json()

            print(results["response"])
            # Prepare the prompt from Jinja template

            # Update the items in the DynamoDB table with the output


        

    # Batch the items into lists of 50 

    # For each batch  
        # call the EC2 Ollama Llama model -> get the output 
        # Update the items in the DynamoDB table with the output

    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }


if __name__ == "__main__":
    lambda_handler({},{})