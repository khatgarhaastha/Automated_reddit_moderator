from utils import submissionNamesFromS3, fetchSubmissions, storingSubmissions, fetchRules, storingRules
import json

def lambda_handler(event, context):
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

    return {
        'statusCode': 200,
        'body': json.dumps('Data fetched and stored successfully!')
    }