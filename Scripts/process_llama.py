import requests

def send_request(url, data):
    # Send request to ec2 instance
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)  # Ensure headers are sent
    return response


def prepare_data(user_input_text, model = "llama3.2"):
    # Prepare data for request
    data = {
        "prompt": user_input_text,
        "stream" : False,
        "model" : model
    }
    return data

# function that will take input from the use and sends that to llama to get the response
def llama_response(text_file):

    data = prepare_data(text_file)
    ec2endpoint = "http://ec2-3-142-92-196.us-east-2.compute.amazonaws.com:11434/api/generate/"
    response = send_request(ec2endpoint, data)
    # Print the response, handling errors if any
    if response.status_code == 200:
        print(response.json().get("response", "No response found"))
    else:
        print(f"Error: {response.status_code}, {response.text}")



# function that will take input from the user
def input_text():
    data = input("Enter the text to be processed: ")
    return data

def main():

    sample_text = input_text()
    data = prepare_data(sample_text)
    ec2endpoint = "http://ec2-3-142-92-196.us-east-2.compute.amazonaws.com:11434/api/generate/"
    response = send_request(ec2endpoint, data)
    # Print the response, handling errors if any
    if response.status_code == 200:
        print(response.json().get("response", "No response found"))
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    sample_text = "mirror mirror on the wall, who is the fairest of them all?"
    llama_response(sample_text)

