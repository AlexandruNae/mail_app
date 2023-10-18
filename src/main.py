import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def update_send():
    # Initialize or load DataFrame
    try:
        df = pd.read_csv("../docs/user_track.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Email', 'LastPage'])

    # Define the book content (Replace this with actual book content)
    book_content = {
        1: "Page 1 content",
        2: "Page 2 content",
        3: "Page 3 content",
        4: "Page 4 content",
        5: "Page 5 content",
        6: "Page 6 content",
        7: "Page 7 content",
        8: "Page 8 content",
        9: "Page 9 content"
    }

    def send_email(user_email, pages):
        # SMTP settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        smtp_user = "alexnaer@gmail.com"
        smtp_password = "aait colq xzma aaib"

        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = user_email
        msg['Subject'] = "Your book pages"

        text = "\n".join([book_content[page] for page in pages])
        msg.attach(MIMEText(text, 'plain'))

        # Send email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, user_email, msg.as_string())


    # List of email addresses (Replace with actual emails)
    # email_list = ["alexnaer@gmail.com"]#, "virgilbaldovin6@gmail.com", "dumitriurobert0@gmail.com"]

    for email in df['Email'].tolist():
        last_page = df[df['Email'] == email]['LastPage'].iloc[0]
        if last_page is None:
            last_page = 0

        next_pages = list(range(last_page + 1, last_page + 3))  # Sending next 5 pages

        # Update tracking
        df.loc[df['Email'] == email, 'LastPage'] = next_pages[-1]

        # Send email
        send_email(email, next_pages)

    # Save DataFrame to CSV
    df.to_csv("docs/user_track.csv", index=False)


