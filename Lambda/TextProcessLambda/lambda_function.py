
# For each subreddit : 

    # Fetch submission from DynamoDB

    # Fetch Rules from DynamoDB

    # Create a prompt to check for analysis of submission rule wise 

    # Return for each submission should be : 

'''

for each submission you generate :

{
Submission Text : "Text of the submission",

Rule_Analysis : [
    {
    Rule : "Rule 1",
    Rule Text : "Rule 1 Text",
    Rule Violated : "Yes/No",
    Rule Violation Reason : "Reason for violation"
    },
    {
    Rule : "Rule 2",
    Rule Text : "Rule 2 Text",
    Rule Violated : "Yes/No",
    Rule Violation Reason : "Reason for violation"
    },
    
]
'''