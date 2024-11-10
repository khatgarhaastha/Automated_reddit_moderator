import boto3
import praw
import json
from botocore.exceptions import ClientError
import csv
import io

'''
SubAIModerator 
id : IRcrs_-VMIOORRX9JjlYsw
secret : 3FeO5woG65TKBAWPap9P4Bmf56cVAA
'''

# In this we are fetching the subreddit names from S3 bucket and storing them in a list

def submissionNamesFromS3(bucket_name, csv_file_key):
    """
    Fetches subreddit names from a CSV file stored in an S3 bucket and returns them as a list.
    
    Parameters:
    - bucket_name: str, name of the S3 bucket
    - csv_file_key: str, key (path/filename) of the CSV file in the bucket
    
    Returns:
    - List of subreddit names
    """
    s3 = boto3.client('s3')
    
    try:
        # Fetch the CSV file object from S3
        response = s3.get_object(Bucket=bucket_name, Key=csv_file_key)
        
        # Read the CSV content from the response body
        csv_content = response['Body'].read().decode('utf-8')
        subreddit_names = []

        # Using csv.reader to parse the CSV content
        csv_reader = csv.reader(io.StringIO(csv_content))
        
        # Assuming each row in the CSV contains a subreddit name
        for row in csv_reader:
            # Append the first column value (subreddit name) from each row
            subreddit_names.append(row[0])
        
        if subreddit_names:
            print(f"Subreddit names fetched successfully from {csv_file_key}.")
        else:
            print("No subreddit names found in the CSV file.")
        
        return subreddit_names
    
    except Exception as e:
        print(f"Error reading the CSV file from S3: {e}")
        return []



# Fetching submissions from Reddit
def fetchSubmissions(subreddit_name):
    """
    Fetches the top submissions from the given subreddit for the past day.
    
    Parameters:
    subreddit_name (str): Name of the subreddit to fetch data from
    
    Returns:
    Dictionary: A dictionary of top submissions from the subreddit with key as submission ID and value as submission text
    """
    # Reading config file for Reddit credentials from JSON file
    #with open('Configs/reddit.json') as f:
        #config = json.load(f)
    
    client_id = 'IRcrs_-VMIOORRX9JjlYsw'
    client_secret = '3FeO5woG65TKBAWPap9P4Bmf56cVAA'
    user_agent = 'reddit_bot_userAgent'
    
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    # Fetching the data from the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Storing submissions in a dictionary with submission id as key and submission text as value
    submissions_dict = {subreddit_name: {}}

    # Fetching the data from the subreddit
    try:
        for submission in subreddit.top(time_filter='day'):
            submissions_dict[subreddit_name][submission.id] = submission.selftext

        if submissions_dict[subreddit_name]:
            print(f"Top submissions fetched successfully from r/{subreddit_name}.")
        else:
            print(f"No submissions found for r/{subreddit_name}.")

    except Exception as e:
        print(f"Error fetching submissions from r/{subreddit_name}: {e}")
        return None

    return submissions_dict # Dictionary of submissions

'''
{
  "subreddit_name": {
    "submission_id_1": "submission_text",
    "submission_id_2": "submission_text"
  }
}

'''


# Fetching subreddit rules
def fetchRules(subreddit_name):
    """
    Fetches the rules of the given subreddit.
    
    Parameters:
    subreddit_name (str): Name of the subreddit to fetch rules from
    
    Returns:
    List: A list of rules of the subreddit
    """
    # Reading config file for Reddit credentials from JSON file
    #with open('Configs/reddit.json') as f:
        #config = json.load(f)
    
    client_id = 'IRcrs_-VMIOORRX9JjlYsw'
    client_secret = '3FeO5woG65TKBAWPap9P4Bmf56cVAA'
    user_agent = 'reddit_bot_userAgent'
    
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    # Fetching the data from the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    subreddit_rules = []
    # Append Rules 
    for rule in subreddit.rules:
        subreddit_rules.append(rule.short_name)

    if subreddit_rules:
        print(f"Rules fetched successfully from r/{subreddit_name}.")
    else:
        print(f"No rules found for r/{subreddit_name}.")

    return subreddit_rules # List of rules


# Storing submissions in the DynamoDB table
def storingSubmissions(subreddit_name, submission_id, submission_text):
    """
    Stores the submission in the DynamoDB table.
    
    Parameters:
    subreddit (str): Name of the subreddit
    submission_id (str): ID of the submission
    submission_text (str): Text of the submission
    
    Returns:
    bool: True if the submission is stored successfully, False otherwise
    """
    # Connecting to the DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('reddit-submissions')

    try:
        # Check if submission with the given ID already exists
        response = table.get_item(Key={'submission_id': submission_id})
        if 'Item' in response:
            print(f"Submission with ID {submission_id} already exists in the table.")
            return False
        
        # Insert the submission into the table
        table.put_item(
            Item={
                'subreddit': subreddit_name,
                'submission_id': submission_id,
                'submission_text': submission_text,
                'processed_nsfw': False,
                'processed_rules': False
            }
        )
        print(f"Submission with ID {submission_id} stored successfully.")
        return True
    except ClientError as e:
        print(f"Error storing submission with ID {submission_id}: {e.response['Error']['Message']}")
        return False
    

# Storing rules in the DynamoDB table
def storingRules(subreddit_name, rules):
    """
    Stores the rules in the DynamoDB table.
    
    Parameters:
    subreddit_name (str): Name of the subreddit
    rules (list): List of rules
    
    Returns:
    bool: True if the rules are stored successfully, False otherwise
    """
    # Connecting to the DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('reddit-subreddit-rules')

    try:
        # Check if rules for the given subreddit already exist
        response = table.get_item(Key={'subreddit': subreddit_name})
        if 'Item' in response:
            print(f"Rules for r/{subreddit_name} already exist in the table.")
            return False
        
        # Insert the rules as a single item in the table
        table.put_item(
            Item={
                'subreddit': subreddit_name,
                'rules': rules
            }
        )
        
        print(f"Rules for r/{subreddit_name} stored successfully.")
        return True
    except ClientError as e:
        print(f"Error storing rules for r/{subreddit_name}: {e.response['Error']['Message']}")
        return False
    

def main():
    # Fetching the subreddit names from the S3 bucket
    bucket_name = 'reddit-moderator-s3'
    csv_file_key = 'top_subreddits_cleaned.csv'

    subreddit_names = submissionNamesFromS3(bucket_name, csv_file_key)
    print(subreddit_names)  

    if not subreddit_names:
        print("No subreddit names found in the S3 bucket.")
        return

    # Fetching submissions and rules for each subreddit
    for subreddit_name in subreddit_names:
        # Fetching the top submissions from the subreddit
        submissions_dict = fetchSubmissions(subreddit_name)

        if not submissions_dict:
            continue

        # Storing the submissions in the DynamoDB table
        submissions_dict = submissions_dict[subreddit_name]
        for submission_id, submission_text in submissions_dict.items():
            if not submission_text:
                continue
            storingSubmissions(subreddit_name, submission_id, submission_text)

        # Fetching the rules of the subreddit
        subreddit_rules = fetchRules(subreddit_name)

        if not subreddit_rules:
            continue

        # Storing the rules in the DynamoDB table
        storingRules(subreddit_name, subreddit_rules)

    print("All subreddit submissions and rules fetched and stored successfully.")






