import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from Email_handler import login, logout, process_email_with_attachments
from Sending_mail import process_json_and_send_emails
import logging
import warnings
# import torch


# os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

# os.environ["CUDA_VISIBLE_DEVICES"] = "2"

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
    json_filepath = '/data/aiuserinj/sarjil/mail_summarizer/task_output2.json'
    process_json_and_send_emails(json_filepath)

if __name__ == "__main__":
    main()
