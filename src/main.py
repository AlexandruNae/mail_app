from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine
import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import smtplib
import ssl
# from config import WEBSITE_URL
# from src.utils import title_to_alias
import requests
from sqlalchemy.orm import sessionmaker


def title_to_alias(input_text):
    title_underscores = input_text.lower().replace("-", "_").replace(" ", "_")
    parts = title_underscores.split('_', 5)
    # If we have less than 6 parts, it means there weren't 5 underscores, return the original string
    if len(parts) < 6:
        return title_underscores
    # Join the parts back together with underscores
    return '_'.join(parts[:5])


WEBSITE_URL = " https://www.microlecturi.ro"
engine = create_engine('mysql+pymysql://root:Pitagora007#1@localhost:3306/micro_lecturi')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)


# Create a SQLAlchemy engine


def check_if_book_finished(book_title, chunk_number):
    # Define the path to the folder
    book_alias = title_to_alias(book_title)
    # folder_path = os.path.join(f'lectures/{book_alias}', book_title)

    next_chunk_path = f'lectures/{book_alias}/{book_alias}_{chunk_number}.txt'

    # Return True if n is greater than the number of .txt files, False otherwise
    return os.path.isfile(next_chunk_path)


def get_content(book_title, chunk_number):
    book_alias = title_to_alias(book_title)
    # if check_if_book_finished(book_title, chunk_number):
    with open(f'lectures/{book_alias}/{book_alias}_{chunk_number}.txt', 'r') as f:
        return f.read()
    # return ''


def send_email(user_email, book_title, current_chunk, subscription_id, book_id):
    if not check_if_book_finished(book_title, current_chunk):
        return
    # SMTP settings
    smtp_server = "smtp.zoho.eu"
    smtp_port = 587
    smtp_user = "contact@microlecturi.ro"
    smtp_password = "Pitagora007#123"

    # Retrieve the content for the current chunk of the book
    content = get_content(book_title, current_chunk)

    # Replace newlines with HTML line breaks for proper email formatting
    content = content.replace("\n", "<br>")

    next_chunk_url = WEBSITE_URL + "/send_next_chunk/" + str(subscription_id)
    cancel_subscription = WEBSITE_URL + "/cancel_subscription/" + str(subscription_id)

    # Check if the next chunk exists
    book_alias = title_to_alias(book_title)
    next_chunk_path = f'lectures/{book_alias}/{book_alias}_{current_chunk + 1}.txt'
    next_chunk_exists = os.path.isfile(next_chunk_path)

    # Path to the email template
    template_path = os.path.join('templates', 'email_template.html')

    # Read the email template
    with open(template_path, 'r') as template_file:
        email_template = template_file.read()

    # Replace placeholders in the template with actual content
    chunks = get_lecture_chunks_from_subscription(book_id)

    email_body = email_template.format(
        book_title=book_title,
        current_chunk=current_chunk,
        content=content,
        next_chunk_url=next_chunk_url,
        cancel_subscription=cancel_subscription,
        website_url=WEBSITE_URL,
        is_last_mail='inline-block' if next_chunk_exists else 'none',
        is_not_last_mail='none' if next_chunk_exists else 'inline-block',
        chunks=chunks
    )

    # # Create the email message
    # msg = MIMEMultipart('alternative')
    # msg['From'] = f'Micro Lecturi <{smtp_user}>'
    # msg['To'] = user_email
    # msg['Subject'] = f"{book_title} - Partea {current_chunk} / {chunks}"
    #
    # # Attach the HTML content
    # msg.attach(MIMEText(email_body, 'html'))
    #
    # # Send the email using SMTP
    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     server.ehlo()  # Identify ourselves to the SMTP server
    #     server.starttls()  # Secure the SMTP connection
    #     server.ehlo()  # Re-identify ourselves over the secure connection
    #     server.login(smtp_user, smtp_password)  # Log in to the SMTP server
    #     server.sendmail(f'Micro Lecturi <{smtp_user}>', user_email, msg.as_string())

    url = "https://api.zeptomail.eu/v1.1/email"

    payload = ("{\n\"from\": { \"address\": \"noreply@microlecturi.ro\"},\n\"to\": [{\"email_address\": {\"address\": "
               "\"" + user_email + "\",\"name\": \"Micro\"}}],\n\"subject\":\"Test Email\","
               "\n\"htmlbody\":\"<div><b>" + email_body + "</b></div>\"\n}")
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "Zoho-enczapikey "
                         "yA6KbHsM6QyhxjkGQ0k91sWKpd1lr6xo2yq14S3rK8YnKdi1j6E51xplJNe6JmTf0IaA6foCbNkTdtu"
                         "/uN5WLZc3YddQKJTGTuv4P2uV48xh8ciEYNYvjZqgArIVFK9JchggCis4RfkoWA==",
    }

    response = requests.request("POST", url, data=payload, headers=headers)


def update_send():
    # Query database to get subscriptions
    query = "SELECT user.email, user.enabled, subscription.current_chunk, " \
            "lecture.title,  subscription.id as subscription_id " \
            "FROM subscription " \
            "JOIN user ON subscription.id_user = user.id " \
            "JOIN lecture ON subscription.id_lecture = lecture.id " \
            "WHERE subscription.is_active = True " \
            "and user.enabled = True"
    df = pd.read_sql(query, engine)

    for index, row in df.iterrows():
        user_email = row['email']
        current_chunk = row['current_chunk']
        enabled = row['enabled']
        subscription_id = row['subscription_id']
        book_title = row['title']

        if enabled == 1:

            send_email(user_email, book_title, current_chunk + 1, subscription_id)

            # Update current_chunk in database update_query = f"""UPDATE subscription SET current_chunk = {current_chunk
            # + 1} WHERE id_user = (SELECT id FROM user WHERE email = '{user_email}') AND id_lecture = (SELECT id FROM
            # lecture WHERE alias = '{book_title}')"""

            # Execute update query
            with engine.connect() as connection:
                # Get user ID from email
                user_id_query = text("SELECT id FROM user WHERE email = :email")
                result = connection.execute(user_id_query, {'email': user_email}).fetchone()
                if not result:
                    print(f"No user found with email {user_email}")
                    continue
                user_id = result[0]

                # Get lecture ID from alias
                lecture_id_query = text("SELECT id FROM lecture WHERE title = :title")
                result = connection.execute(lecture_id_query, {'title': book_title}).fetchone()
                if not result:
                    print(f"No lecture found with alias {book_title}")
                    continue
                lecture_id = result[0]

                try:
                    update_query = text("""UPDATE subscription
                                           SET current_chunk = :new_chunk
                                           WHERE id_user = :user_id AND id_lecture = :lecture_id""")
                    result = connection.execute(update_query, {'new_chunk': current_chunk + 1, 'user_id': user_id,
                                                               'lecture_id': lecture_id})

                    if result.rowcount == 0:
                        print("No rows were updated. Check if user_id and lecture_id are correct.")

                    connection.commit()
                except SQLAlchemyError as e:
                    print(f"An error occurred: {e}")
                    connection.rollback()


def get_lecture_chunks_from_subscription(lecture_id):
    session = Session()
    try:
        subscription_query = text("""
            SELECT lecture.chunks
            FROM lecture
            WHERE lecture.id = :lecture_id
        """)

        result = session.execute(subscription_query, {'lecture_id': lecture_id}).fetchone()
        session.close()

        # Check if the query returned a result
        if result:
            # Since 'fetchone' returns a tuple, you can access the first element directly
            return result[0]
        else:
            print(f"No lecture chunks found for lecture ID {lecture_id}")
            return None

    except SQLAlchemyError as e:
        session.close()
        print(f"An error occurred when fetching lecture chunks: {e}")
        return None


if __name__ == '__main__':
    update_send()
