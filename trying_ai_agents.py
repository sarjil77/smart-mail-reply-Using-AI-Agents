from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
import json
# import torch
# import logging
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Check if CUDA is available
# if torch.cuda.is_available():
#     device = torch.device("cuda")  # Use the first GPU available
#     print('Using GPU')
#     logging.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
# else:
#     device = torch.device("cpu")
#     print('Using CPU')
#     logging.info("No GPU available, using CPU.")

model = Ollama(model="llama3.1:8b")

email = 'nigerian prince sending some gold'

classifier = Agent(
    role='email classifier', 
    goal='accurately classify the mails based on their importance, give every email one of these ratings: important, casual, or spam', 
    backstory='You are an AI assistant whose job is to classify emails accurately and honestly.',
    verbose=True,
    allow_delegation=False,
    llm=model
)

responder = Agent(
    role='email responder', 
    goal='''Based on the importance of the mail, write a simple response. If the mail is rated 'important' write a formal
    response and if the mail is rated as 'spam' ignore the email, and if the response is 'casual' then write a casual response''', 
    backstory='You are an AI assistant whose job is to write short responses to emails based on their importance provided by the \'classifier\' agent.',
    verbose=True,
    allow_delegation=False,
    llm=model
)

classify_email = Task(
    description=f"summarize the following email: '{email}'",
    agent=classifier,
    expected_output="one of these three options: 'important','spam' or 'casual'",
    output_format='json'
)

respond_to_email = Task(
    description=f"respond to emails: '{email}'",
    agent=responder,
    expected_output="A short response to the email based on the importance provided by the 'classifier' agent",
    output_format='json'
)

crew_classifier = Crew(
    agents=[classifier, responder],
    tasks=[classify_email, respond_to_email],
    verbose=True,
    full_output=True,
    process=Process.sequential
)

crew_classifier.kickoff()

# Access the actual JSON output
classify_email_json_output = classify_email.output.raw
respond_email_json_output = respond_to_email.output.raw

# Manually format the outputs into JSON
output_json = {
    "email": email,
    "classification": classify_email_json_output,
    "response": respond_email_json_output
}
# print(output_json)
print('Here is the output:', json.dumps(output_json, indent=2))
