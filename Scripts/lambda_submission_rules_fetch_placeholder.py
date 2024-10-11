

# Fetch the CSV containing the Subreddit names from S3 


# For each subreddit 
    # Get the submissions from the subreddit (top submissions of the day)
    # Filter for submission that you haven't already fetched (Check the Dynamo DB Submissions table)
    # Connect to Dynamo DB Submsission table 
    # Insert the submissions into the Dynamo DB table

    # Get rules for this subreddit 
    # Connect to Dynamo DB Rules table
    # Insert the rules into the Dynamo DB table

