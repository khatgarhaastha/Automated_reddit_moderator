from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

from pymongo import MongoClient

from tqdm import tqdm

def main():
    llm = Ollama(model="llama2")
    #chat_model = ChatOllama()

    
    # Connecting to the MongoDB
    client = MongoClient("mongodb+srv://bhavinmongocluster.5t6smyb.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
                    tls=True,
                    tlsCertificateKeyFile='./Certs/X509-cert-4153501619407879612.pem')
    
    
    db = client['mainDB']
    collection_submission = db['RedditSubmissions']
    collection_comments = db['RedditComments']
    collection_rules = db['RedditRules']

    subreddit = "explainlikeimfive"

    # Fetch the rules for the subreddit 
    
    rules = []
    response = collection_rules.find({'subreddit':subreddit})

    for i, rule in enumerate(response): 
        rules.append(str(i+1) +". "+ rule['rule'])

    rules = "\n".join(rules)

    #print(rules)
    # Fetch the submissions from the subreddit
    submissions = []
    response = collection_submission.find({'subreddit':subreddit})

    for i,submission in enumerate(response):
        submissions.append(submission['submission_text'])
    
    
    #print(submissions)


    prompt = PromptTemplate.from_template("You are a Reddit Moderator Helper! Your job is to read the submissions which can be either posts or Comments and check if they are appropriate or not. You will be given Rules for the subreddit. For each rule presented, you have to analyse if the given submission is in violation of the rule. As final response, you will have to provide pointwise commentary for each rule and give your opinion on whether the submission violated the rule. If the submission is in clear violation of given rule, State the same with assertive negative sentiment comment for the rule. If not, then you can respond in a positive sentiment comment for the rule. For final response for each submission, you have to start the answer with number of rules the post violates. Then mention the rules that are being violated and commentary as to why you think the rules were violated.\n  Here are the rules : {rules} . Here is the submission : {submission} ")
    count = 0
    responses = []
    chain = prompt | llm 
    for submission in tqdm(submissions):
        count += 1
        responses.append(chain.invoke({"submission": submission, "rules" : rules}))

        if(count == 10):
            break
        
    # save the responses and the submission on disk 
        
    with open("Responses.txt", "w", encoding="utf-8") as f:
        for i in range(len(responses)):
            f.write("Submission : " + submissions[i] + "\n")
            f.write("Response : " + responses[i] + "\n")
            f.write("\n\n\n")
    pass

if __name__ == '__main__':
    main()