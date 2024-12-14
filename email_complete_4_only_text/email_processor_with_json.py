import os
import json
import uuid
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def read_email_contents(file_path):
    """Reads the contents of the email file and returns a list of email contents."""
    with open(file_path, "r") as file:
        content = file.read()
    # Split the content into individual emails based on the separator
    emails = content.split("==================================================")
    return [email.strip() for email in emails if email.strip()]

def extract_email_metadata(email_content):
    """Extracts metadata and body from the email content."""
    email_lines = email_content.split("\n")
    email_from = email_lines[0].replace("From: ", "").strip()
    email_subject = email_lines[1].replace("Subject: ", "").strip()
    email_body = "\n".join(email_lines[3:]).strip()
    return email_from, email_subject, email_body

def create_classifier_agent(model):
    """Creates and returns a classifier agent."""
    return Agent(
        role='email classifier',
        goal='accurately classify emails. Give one of these ratings: important, casual, spam',
        backstory='you are an AI assistant whose only job is to classify emails accurately and give a bad rating if the content of the mail is bad',
        verbose=False,
        allow_delegation=False,
        llm=model
    )

def create_responder_agent(model):
    """Creates and returns a responder agent."""
    return Agent(
        role='email responder',
        goal='based on the importance of an email, write a concise and simple response. If the email is rated "important" write a formal response, if the email is rated "casual" write a casual response, and if the mail is rated "spam" write a response that why you rated it as spam',
        backstory='you are an AI assistant whose job is to provide short responses to emails based on their importance. The importance will be provided to you by the "classifier" agent',
        verbose=False,
        allow_delegation=False,
        llm=model
    )

def create_tasks(email_body, classifier, responder):
    """Creates and returns the classification and response tasks."""
    classify_email = Task(
        description=f'classify the email: {email_body}',
        agent=classifier,
        expected_output="one of the three outputs: 'important', 'casual', 'spam'",
        # output_format="json"  # Set the output format to JSON
    )

    respond_to_email = Task(
        description=f"respond to the email: '{email_body}' based on the importance provided by the 'classifier' agent",
        agent=responder,
        expected_output="a very concise response to the email based on the importance provided by the 'classifier' agent",
        # output_format="json"  # Set the output format to JSON
    )

    return classify_email, respond_to_email

def process_emails(file_path):
    """Main function to process multiple emails."""
    # Read the email contents from the file
    email_contents = read_email_contents(file_path)

    # Instantiate the Ollama model with llama3.1
    model = Ollama(model="llama3.1:8b")

    # Define the agents
    classifier = create_classifier_agent(model)
    responder = create_responder_agent(model)

    all_results = []

    for email_content in email_contents:
        # Extract email metadata and body
        email_from, email_subject, email_body = extract_email_metadata(email_content)

        # Define the tasks
        classify_email, respond_to_email = create_tasks(email_body, classifier, responder)

        # Create the crew
        crew = Crew(
            agents=[classifier, responder],
            tasks=[classify_email, respond_to_email],
            verbose=0,
            full_output=True,
            process=Process.sequential
        )

        result = crew.kickoff()

        # Parse the outputs as JSON
        classify_email_output = json.loads(classify_email.output.json())
        respond_to_email_output = json.loads(respond_to_email.output.json())

        # Format the outputs as readable JSON
        formatted_classifier_output = classify_email_output  # Already in dictionary form
        formatted_responder_output = respond_to_email_output  # Already in dictionary form

        # print('Classifier Output:', json.dumps(formatted_classifier_output, indent=4))
        # print('Responder Output:', json.dumps(formatted_responder_output, indent=4))

        # Log the sources of the outputs
        logging.info(f"Classifier Output: {json.dumps(formatted_classifier_output, indent=4)}")
        logging.info(f"Responder Output: {json.dumps(formatted_responder_output, indent=4)}")

        # Generate a unique ID for this email
        email_id = str(uuid.uuid4())

        # Append the results with unique ID
        email_result = {
            "ID": email_id,
            "From": email_from,
            "Subject": email_subject,
            "Content": email_body,
            "Classifier Output": formatted_classifier_output,
            "Responder Output": formatted_responder_output
        }

        all_results.append(email_result)

    # Save all results to a JSON file
    output_filepath = '/data/aiuserinj/sarjil/mail_summarizer/task_output.json'

    try:
        with open(output_filepath, 'w') as json_file:
            json.dump(all_results, json_file, indent=4)
        logging.info(f"Results saved to {output_filepath}")
    except Exception as e:
        logging.error(f"Failed to save results to {output_filepath}. Error: {str(e)}")

if __name__ == "__main__":
    process_emails("inbox_email_content.txt")
