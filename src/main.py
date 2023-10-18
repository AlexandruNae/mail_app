from sqlalchemy import create_engine
import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import text

# Create a SQLAlchemy engine
engine = create_engine('mysql+pymysql://root:Pitagora007#1@localhost:3306/micro_lecturi')


def get_content(book_alias, chunk_number):
    with open(f'lectures/{book_alias}/{book_alias}_{chunk_number}.txt', 'r') as f:
        return f.read()


def send_email(user_email, book_alias, current_chunk):
    # SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = "alexnaer@gmail.com"
    smtp_password = "aait colq xzma aaib"

    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = user_email
    msg['Subject'] = f"Your book chunk for {book_alias}"

    text = get_content(book_alias, current_chunk)
    # text = text + '\n\n\n\n' + f"Click here to get the next chunk: {next_chunk_url}"
    msg.attach(MIMEText(text, 'plain'))


    # Send email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, user_email, msg.as_string())


def update_send():
    # Query database to get subscriptions
    query = "SELECT user.email, user.enabled, subscription.current_chunk, lecture.alias " \
            "FROM subscription " \
            "JOIN user ON subscription.id_user = user.id " \
            "JOIN lecture ON subscription.id_lecture = lecture.id " \
            "WHERE subscription.is_active = True " \
            "and user.enabled = True"
    df = pd.read_sql(query, engine)



    for index, row in df.iterrows():
        user_email = row['email']
        book_alias = row['alias']
        current_chunk = row['current_chunk']
        enabled = row['enabled']

        if enabled == 1:
            send_email(user_email, book_alias, current_chunk)

            # Update current_chunk in database update_query = f"""UPDATE subscription SET current_chunk = {current_chunk
            # + 1} WHERE id_user = (SELECT id FROM user WHERE email = '{user_email}') AND id_lecture = (SELECT id FROM
            # lecture WHERE alias = '{book_alias}')"""

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
                lecture_id_query = text("SELECT id FROM lecture WHERE alias = :alias")
                result = connection.execute(lecture_id_query, {'alias': book_alias}).fetchone()
                if not result:
                    print(f"No lecture found with alias {book_alias}")
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


if __name__ == '__main__':
    update_send()