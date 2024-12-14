# from email_handler import login, logout, process_email_with_attachments --> this do not contain time of the received mail
from email_handler_aug18 import login, logout, process_email_with_attachments
from email_sender_with_specific_attach import process_json_and_send_emails
import logging
import warnings
import os 


os.environ["CUDA_VISIBLE_DEVICES"] = "2"

warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def main():
    # Login to email
    logging.info("Logging in to your IMAP server...")
    login()
    
    try:    
        # Process emails and save results to JSON
        process_email_with_attachments()
    finally:
        # Logout from email
        logout()
        logging.info("Succesfully Logged out from the server.")
        logging.info("Fetched emails and saved its results from classifier and responder ")


    # Send processed email results
    json_filepath = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/all_email_results.json'
    process_json_and_send_emails(json_filepath)

if __name__ == "__main__":
    main()
