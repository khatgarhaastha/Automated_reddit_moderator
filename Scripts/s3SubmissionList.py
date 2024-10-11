import boto3
import praw
import json
from botocore.exceptions import ClientError

# In this we are fetching the subreddit names from S3 bucket and storing them in a list
def submissionNamesFromS3(bucket_name):
    s3 = boto3.client('s3')
    
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)

        subreddit_names = []
        if "Contents" in response:
            for obj in response["Contents"]:
                subreddit_names.append(obj["Key"])
        else: 
            print("No submissions found in the bucket")
            return []
    except Exception as e:
        print(e)
        return []
    
    return subreddit_names # List of subreddit names


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
    with open('Configs/reddit.json') as f:
        config = json.load(f)
    
    client_id = config["reddit_bot_id"]
    client_secret = config['reddit_bot_secret']
    user_agent = config['reddit_bot_userAgent']
    
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
    with open('Configs/reddit.json') as f:
        config = json.load(f)
    
    client_id = config["reddit_bot_id"]
    client_secret = config['reddit_bot_secret']
    user_agent = config['reddit_bot_userAgent']
    
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
                'submission_text': submission_text
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
    subreddit_names = submissionNamesFromS3(bucket_name)
    print (subreddit_names)
'''
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
        for submission_id, submission_text in submissions_dict.items():
            storingSubmissions(subreddit_name, submission_id, submission_text)

        # Fetching the rules of the subreddit
        subreddit_rules = fetchRules(subreddit_name)

        if not subreddit_rules:
            continue

        # Storing the rules in the DynamoDB table
        storingRules(subreddit_name, subreddit_rules)

    print("All subreddit submissions and rules fetched and stored successfully.")




'''
    
if __name__ == "__main__":
    main()
