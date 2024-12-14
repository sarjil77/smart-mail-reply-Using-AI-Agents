import email_fetcher
import email_processor_with_json
import error_solving_related_to_json
import email_sender
import logging

# Configure logging
logging.basicConfig(filename='logging_for_mail.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S')

def main():
    # Step 1: Fetch and save emails
    email_fetcher.fetch_and_save_emails("inbox_email_content.txt")

    # Step 2: Process the email content and save AI agent responses
    # email_processor_with_json.process_emails("inbox_email_content.txt")
    error_solving_related_to_json.process_emails("inbox_email_content.txt")

    # Step 3: Send the response email based on AI agent output
    email_sender.send_responses_from_json('/data/aiuserinj/sarjil/mail_summarizer/email_complete_4_only_text/task_output2.json', 'youremail@gmail.com')

if __name__ == "__main__":
    main()
