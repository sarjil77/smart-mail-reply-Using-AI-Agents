import imaplib
import email
from email.header import decode_header
import json

email_user = "xyz@gmail.com"
email_pass = "958 bolt a champion"


# Initialize IMAP client
def init_imap():
    return imaplib.IMAP4_SSL("imap.gmail.com")

def login(imap):
    if imap.state == 'LOGOUT':
        imap = init_imap()  # Reinitialize if in LOGOUT state
    imap.login(email_user, email_pass)
    return imap

def logout(imap):
    imap.close()
    imap.logout()

def fetch_unseen_email_count():
    imap = init_imap()
    imap = login(imap)
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    logout(imap)
    return len(email_ids)

if __name__ == "__main__":
    print(fetch_unseen_email_count())
