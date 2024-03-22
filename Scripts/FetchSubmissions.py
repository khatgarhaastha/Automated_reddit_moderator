
import praw
import json
from pymongo import MongoClient

import datetime as dt

def main():
    print("Fetching the Reddit Data....")
    subreddit_name = 'explainlikeimfive'

    # Reading config file for reddit credentials from JSON file
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
    
    # Define the time period you want to fetch posts from
    end_time = int(dt.datetime.now().timestamp())
    start_time = end_time - 24*60*60  # 24 hours before end_time

    submissions = []
    # Fetching the data from the subreddit
    for submission in subreddit.top(time_filter='day'):
        submissions.append(submission)

    if(len(submissions)>0):
        print("Submissions Fetch Successfully....")
    else:
        print("No Submissions Found....")

    print("===============================================")

    # Connecting to the MongoDB
    client = MongoClient("mongodb+srv://bhavinmongocluster.5t6smyb.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
                    tls=True,
                    tlsCertificateKeyFile='./Certs/X509-cert-4153501619407879612.pem')
    
    
    db = client['mainDB']
    collection_submission = db['RedditSubmissions']
    collection_comments = db['RedditComments']
    # Inserting the data into the MongoDB
    for submission in submissions:

        # Check if the submission is already present in the database
        if collection_submission.find_one({'submission_id':submission.id}):
            print("Submission already present in the database....")
            continue
        
        # Insert the submission into the database
        collection_submission.insert_one({
            'subreddit':subreddit_name,
            'submission_id':submission.id, 
            'submission_name': submission.name, 
            'submission_title':submission.title, 
            'submission_text': submission.selftext
            })
        print("Submission Inserted Successfully....")

        # Adding comments from the submission
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            # Check if the comment is already present in the database
            if collection_comments.find_one({'comment_id':comment.id}):
                print("Comment already present in the database....")
                continue

            collection_comments.insert_one({
                'submission_id':submission.id,
                'comment_id':comment.id,
                'comment_text':comment.body
            })
        
        print("Comments Inserted Successfully....")


    print("Data Inserted Successfully....")
    print("===============================================")

    client.close()

if __name__ == '__main__':
    main()

