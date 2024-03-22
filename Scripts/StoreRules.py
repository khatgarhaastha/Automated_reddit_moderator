
import praw
import json
from pymongo import MongoClient

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
    
    rules = []
    # Print Rules 
    for rule in subreddit.rules:
        rules.append(rule.short_name)




    if(len(rules)>0):
        print("Rules Fetch Successfully....")
    else:
        print("No Rules Found....")

    print("===============================================")
    
    print("Storing the Data into MongoDB....")

    # Connecting to the MongoDB
    client = MongoClient("mongodb+srv://bhavinmongocluster.5t6smyb.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
                    tls=True,
                    tlsCertificateKeyFile='./Certs/X509-cert-4153501619407879612.pem')
    
    
    db = client['mainDB']
    collection = db['RedditRules']

    # Inserting the data into the MongoDB
    for rule in rules:
        collection.insert_one({'subreddit':subreddit_name, 'rule':rule})   

    print("Data Inserted Successfully....")
    print("===============================================")

    client.close()

if __name__ == '__main__':
    main()

