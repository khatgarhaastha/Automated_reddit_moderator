import streamlit as st

def parse_responses(file_path):
    """
    Parses the provided text file into a list of dicts with 'submission' and 'response' keys,
    accounting for multi-paragraph submissions and responses.
    """
    submissions_responses = []
    current_submission = ""
    current_response = ""
    reading_submission = False
    reading_response = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Submission :"):
                if current_submission or current_response:  # Save the previous pair if exists
                    submissions_responses.append({"submission": current_submission.strip(), "response": current_response.strip()})
                    current_submission = ""
                    current_response = ""
                current_submission = line.replace("Submission :", "").strip()
                reading_submission = True
                reading_response = False
            elif line.startswith("Response :"):
                current_response = line.replace("Response :", "").strip()
                reading_response = True
                reading_submission = False
            elif reading_submission:
                current_submission += " " + line.strip()
            elif reading_response:
                current_response += " " + line.strip()

        # Add the last submission-response pair if the file doesn't end with multiple newlines
        if current_submission or current_response:
            submissions_responses.append({"submission": current_submission.strip(), "response": current_response.strip()})

    return submissions_responses

def create_dashboard(submissions_responses):
    """
    Creates a Streamlit dashboard with expandable cards for each submission-response pair.
    """
    st.title("Submissions and Responses Dashboard")

    for i, item in enumerate(submissions_responses):
        with st.expander(f"Submission {i+1}"):
            st.markdown(f"**Submission:**\n{item['submission']}")

            # Format response to add new line where the string starts with "Rule <Any Number>"
            response = item["response"].replace("Rule ", "\n - Rule ")
            st.markdown(f"**Response:**\n{response}")

if __name__ == "__main__":
    file_path = "Responses.txt"
    submissions_responses = parse_responses(file_path)
    create_dashboard(submissions_responses)
