import os 
from dotenv import load_dotenv

load_dotenv()

def generate_nsfw_flags(limit):
    #get url from the env 
    url = os.getenv('NSFW_PARSER_URL')

    data = {
        'limit': limit
    }


def process_llama():
    pass
