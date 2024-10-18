import imaplib
import email
from datetime import datetime

server = "imap.gmail.com"
user = "<Your mail id>"
pas = "<your mail password from app passwords>"

imap = imaplib.IMAP4_SSL(server)
imap.login(user, pas)
imap.select("INBOX")

status, msgnums = imap.search(None, "ALL")
print(f"Search Status: {status}")
print(f"Message Numbers: {msgnums}")

email_ids = msgnums[0].split()

if not email_ids:
    print("No emails found.")
else:
    print(f"Total Emails: {len(email_ids)}")

emails_with_dates = []

for msgnum in email_ids:
    print(f"Fetching email ID: {msgnum.decode()}")
    status, data = imap.fetch(msgnum, "(RFC822)")

    if status != "OK":
        print(f"Error fetching email ID: {msgnum.decode()}")
        continue

    raw_email = data[0][1]
    message = email.message_from_bytes(raw_email)
    
    email_date = message.get('Date')
    date_tuple = email.utils.parsedate_tz(email_date)
    
    if date_tuple:
        local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        emails_with_dates.append((msgnum, local_date, message))
        print(f"Email fetched successfully. Date: {local_date}")
    else:
        print(f"Error parsing date for email ID: {msgnum.decode()}")

emails_with_dates.sort(key=lambda x: x[1], reverse=True)
recent_five_emails = emails_with_dates[:5]

for msgnum, date, message in recent_five_emails:
    print(f"Message Number: {msgnum.decode()}")
    print(f"Message From: {message.get('From')}")
    print(f"Message To: {message.get('To')}")
    print(f"Date: {message.get('Date')}")
    print(f"Subject: {message.get('Subject')}")

    print("Content: ")
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            print(part.get_payload(decode=True).decode('utf-8', errors='ignore'))

imap.close()
imap.logout()

