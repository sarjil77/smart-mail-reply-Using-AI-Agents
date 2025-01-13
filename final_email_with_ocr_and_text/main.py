import logging
from email_handler_aug20_1 import process_emails_from_json
from email_sender_with_specific_attach import process_json_and_send_emails

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Step 1: Process the emails from the JSON file
    logging.info("Starting the email processing workflow...")
    process_emails_from_json()
    
    # Step 2: Send the emails based on the processed results
    json_output_path = 'your_path/mail_summarizer/final_email_with_ocr_and_text/all_email_results_aug_18.json'
    logging.info("Sending email responses...")
    process_json_and_send_emails(json_output_path)

    logging.info("Workflow completed successfully.")

if __name__ == "__main__":
    main()
