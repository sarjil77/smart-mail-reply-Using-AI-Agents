import imaplib
import email
from email.header import decode_header
import os
import boto3
import json
# import torch
import uuid
import tempfile
from pdf2image import convert_from_path
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from crewai.tasks.output_format import OutputFormat
import logging
from AI_agents import create_classifier_agent, create_image_summarizer_agent, create_pdf_summarizer_agent,create_email_responder


# device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Email credentials
email_user = "xyz@gmail.com"
email_pass = "958 bolt a champion"

# yuor ocr 

# Paths
attachment_save_path = "/data/aiuserinj/sarjil/mail_summarizer/handling_attachments"

# Initialize IMAP client
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Initialize AWS Textract client
textract_client = boto3.client('textract', 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key, 
                               region_name='us-east-1')

def login():
    print("Logging in...")
    imap.login(email_user, email_pass)
    print("Logged in.")

def logout():
    print("Logging out...")
    imap.close()
    imap.logout()
    print("Logged out.")

def fetch_unseen_emails():
    print("Fetching unseen emails...")
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    print(f"Unseen emails fetched: {messages[0].split()}")
    return messages[0].split()

def extract_text_from_image(image_path):
    print(f"Extracting text from image: {image_path}")
    with open(image_path, 'rb') as img_file:
        response = textract_client.detect_document_text(Document={'Bytes': img_file.read()})
        text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + "\n"
    print(f"Extracted text from image: {text[:100]}...")  # print the first 100 characters 
    return text

def extract_text_from_pdf_as_images(pdf_path):
    print(f"Extracting text from PDF as images: {pdf_path}")
    text = ""
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_path, output_folder=path)
        for i, image in enumerate(images):
            image_path = os.path.join(path, f"page_{i}.jpg")
            image.save(image_path, 'JPEG')
            text += extract_text_from_image(image_path)
    print(f"Extracted text from PDF: {text[:100]}...")  # Print the first 100 characters for brevity
    return text

def save_attachment(part, filename):
    print(f"Saving attachment: {filename}")
    filepath = os.path.join(attachment_save_path, filename)
    with open(filepath, "wb") as f:
        f.write(part.get_payload(decode=True))
    print(f"Attachment saved at: {filepath}")
    return filepath

def process_email_with_attachments():
    print("Processing emails with attachments...")
    messages = fetch_unseen_emails()

    # List to hold results of all emails
    all_email_results = []

    # RFC822 is IMAP command for getting all the raw content of the mail
    for mail in messages:
        _, msg_data = imap.fetch(mail, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = decode_header(msg["subject"])[0][0]
                email_from = decode_header(msg["from"])[0][0]
                print(f"Processing email - Subject: {email_subject}, From: {email_from}")

                email_content = ""
                image_files = []
                pdf_files = []

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            if filename:
                                filepath = save_attachment(part, filename)
                                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                                    image_files.append(filepath)
                                elif filename.lower().endswith(".pdf"):
                                    pdf_files.append(filepath)
                        else:
                            # Extract text from non-attachment parts of the email
                            try:
                                email_content += part.get_payload(decode=True).decode()
                            except:
                                pass  # Skip if decoding fails
                else:
                    # Single part email, extract content directly
                    email_content = msg.get_payload(decode=True).decode()

                # Define AI agents
                print("Defining AI agents...")
                model = Ollama(model="llama3.1:8b")
                classifier = create_classifier_agent(model)
                responder = create_email_responder(model)
                image_summarizer = create_image_summarizer_agent(model)
                pdf_summarizer = create_pdf_summarizer_agent(model)
                
                # Process image files
                print(f"Image files to process: {image_files}")
                image_ocr_results = []
                for image_file in image_files:
                    ocr_content = extract_text_from_image(image_file)
                    # Define tasks for images
                    classify_image_task = Task(
                        description=f'Summarize the OCR content from the image: {ocr_content}',
                        agent=image_summarizer,
                        expected_output='A concise summary of the OCR content in 2-3 sentences, identifying key points and the type of attachment (e.g., policy document, claim form, etc.).',
                        # output_format = OutputFormat.JSON,
                        # output_json=True
                        # output_format="json"
                    )
                    # Create and run the crew for image summarization
                    crew_image = Crew(
                        agents=[image_summarizer],
                        tasks=[classify_image_task],
                        verbose=0,
                        full_output=True,
                        process=Process.sequential
                    )
                    result_image = crew_image.kickoff()
                    summarize_image_output = classify_image_task.output.raw
                    image_ocr_results.append({
                        "Image File": image_file,
                        "Summary": summarize_image_output
                    })

                # Process PDF files
                print(f"PDF files to process: {pdf_files}")
                pdf_ocr_results = []
                for pdf_file in pdf_files:
                    ocr_content = extract_text_from_pdf_as_images(pdf_file)
                    # Define tasks for PDFs
                    classify_pdf_task = Task(
                        description=f'Summarize the content of the PDF document: {ocr_content}',
                        agent=pdf_summarizer,
                        expected_output='A concise summary of the PDF content in 2-3 sentences, identifying key points and the type of attachment (e.g., policy document, claim form, etc.).',
                        # output_format = OutputFormat.JSON,
                        # output_json=True
                        # output_format="json"
                    )
                    # Create and run the crew for PDF summarization
                    crew_pdf = Crew(
                        agents=[pdf_summarizer],
                        tasks=[classify_pdf_task],
                        verbose=0,
                        full_output=True,
                        process=Process.sequential
                    )
                    result_pdf = crew_pdf.kickoff()
                    summarize_pdf_output = classify_pdf_task.output.raw
                    pdf_ocr_results.append({
                        "PDF File": pdf_file,
                        "Summary": summarize_pdf_output
                    })

                # Define and run the classifier task
                print("Defining classifier task...")
                classify_email_task = Task(
                    description=f'Classify the email content: {email_content}',
                    agent=classifier,
                    expected_output="one of the following categories: 'Policy Inquiries', 'Claims', 'Billing and Payments', 'Customer Support', 'Renewals', 'Documentation', 'Quotes', 'Cancellations', 'Compliance and Legal', 'Marketing and Promotions', 'Internal Communications'",
                    # output_format="json"
                    # output_format = OutputFormat.JSON,
                    # output_json=True
                )
                crew_classifier = Crew(
                    agents=[classifier],
                    tasks=[classify_email_task],
                    verbose=0,
                    full_output=True,
                    process=Process.sequential
                )
                result_classifier = crew_classifier.kickoff()
                classify_email_output = classify_email_task.output.raw

                # try:
                #     classify_email_output_decoded = json.loads(classify_email_output)
                # except json.JSONDecodeError:
                #     classify_email_output_decoded = classify_email_output


                # Define and run the classifier task
                print("Defining responder task...")
                responder_email_task = Task(
                    description=f'respond to the email content: {email_content}',
                    agent=responder,
                    expected_output="a very concise response to the email based on the importance provided by the 'classifier' agent",
                    # output_format="json"
                    # output_format = OutputFormat.JSON,
                    # output_json=True
                )
                crew_responder = Crew(
                    agents=[responder],
                    tasks=[responder_email_task],
                    verbose=0,
                    full_output=True,
                    process=Process.sequential
                )
                result_responder = crew_responder.kickoff()
                responder_email_output = responder_email_task.output.raw

                # print('Classifier Output:', json.dumps(classify_email_output, indent=4))
                # print('Responder Output:', json.dumps(responder_email_output, indent=4))

                # try:
                #     responder_email_output_decoded = json.loads(responder_email_output)
                # except json.JSONDecodeError:
                #     responder_email_output_decoded = responder_email_output

                # Generate a unique ID for this email
                email_id = str(uuid.uuid4())

                # Append the results with unique ID
                email_result = {
                    "ID": email_id,
                    "From": email_from,
                    "Subject": email_subject,
                    "Content": email_content,
                    "Classifier Output": classify_email_output,
                    "Responder Output": responder_email_output,
                    "Attachments": {
                        "Images": image_ocr_results,
                        "PDFs": pdf_ocr_results
                    }
                }

                # Append the result to the list
                all_email_results.append(email_result)

    # Save all results to a single JSON file
    output_filepath = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/all_email_results.json'
    print('Saving all results to:', output_filepath)
    try:
        with open(output_filepath, 'w') as json_file:
            json.dump(all_email_results, json_file, indent=4)
        logging.info(f"All results saved to {output_filepath}")
    except Exception as e:
        logging.error(f"Failed to save all results to {output_filepath}. Error: {str(e)}")

if __name__ == "__main__":
    login()
    process_email_with_attachments()
    logout()
