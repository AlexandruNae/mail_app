import sqlalchemy
from flask import Flask, request, render_template, url_for, redirect
from datetime import datetime
import pandas as pd
from extensions import db
import os
from src.main import update_send
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from web.models import Lecture, LectureCategory, User, Subscription
from src.main import send_email

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():

    lecture_categories = LectureCategory.query.all()
    category_names = {category.name: category.id for category in lecture_categories}

    genre = request.args.get('genre', default="Toate")
    if genre in category_names and genre != "Toate":
        lectures = Lecture.query.filter_by(id_category=category_names[genre]).all()
    else:
        lectures = Lecture.query.all()
        genre = "Toate"

    return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories, selected_genre=genre)


@app.route('/books/search', methods=['GET'])
def search_lectures():
    query = request.args.get('search')

    lecture_categories = LectureCategory.query.all()

    if not query:
        # If no query is given, fetch all lectures and redirect to the homepage
        lectures = Lecture.query.all()
        return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories,
                               selected_genre="Toate")

    # Filter lectures by title or author
    lectures = Lecture.query.filter(
        or_(Lecture.title.ilike(f"%{query}%"), Lecture.author.ilike(f"%{query}%"))
    ).all()

    # Return the same index.html but with the filtered lectures or all lectures if no results are found
    if not lectures:
        lectures = Lecture.query.all()
        no_results = True
    else:
        no_results = False

    return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories,
                           selected_genre="Toate", no_results=no_results, query=query)


@app.route('/lecture/<book_id>', methods=['GET', 'POST'])
def lecture(book_id):
    # Fetch the lecture object from the database
    current_lecture = db.session.query(Lecture).filter_by(id=book_id).first()

    # Ensure that the lecture exists
    if not current_lecture:
        return "Lecture not found", 404

    message = ""  # Initialize an empty message

    if request.method == 'POST':
        email = request.form['email']
        existing_user = db.session.query(User).filter_by(email=email).first()

        # If user does not exist, create one
        if existing_user is None:
            new_user = User(email=email, enabled=True)
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.id
        else:
            user_id = existing_user.id

        # Check for existing subscription for this user and this lecture
        existing_subscription = db.session.query(Subscription).filter_by(id_user=user_id, id_lecture=book_id).first()

        if existing_subscription:
            # The user is already subscribed, so set an error message
            message = "Esti deja abonat la aceasta lectura."
        else:
            # Add subscription to the 'subscription' table
            new_subscription = Subscription(
                id_user=user_id,
                id_lecture=book_id,
                start_date=datetime.now(),
                current_chunk=1,
                is_active=True
            )
            db.session.add(new_subscription)
            db.session.commit()
            send_email(email, current_lecture.title, 1, new_subscription.id)
            # After successful subscription, redirect to index or another success page
            return redirect(url_for('index'))

    return render_template('lecture.html', book_id=book_id, lecture=current_lecture, message=message)




@app.route('/send_next_chunk/<int:subscription_id>', methods=['GET'])
def send_next_chunk(subscription_id):
    # Fetch the subscription from the database
    subscription = db.session.get(Subscription, subscription_id)

    if not subscription:
        return "Subscription not found!", 404

    # Access the user and lecture directly from the subscription
    user = subscription.user
    lecture = subscription.lecture

    # Ensure both user and lecture are present (though this should always be true if the subscription exists)
    if not user or not lecture:
        return "User or lecture not found!", 404

    current_chunk = subscription.current_chunk

    # Check if the current_chunk is less than the total number of chunks
    if current_chunk >= lecture.chunks:
        return "No more chunks to send!", 400

    # Update the current_chunk in the database
    subscription.current_chunk = current_chunk + 1
    db.session.commit()

    # Send an email with the new chunk

    send_email(user.email, lecture.title, current_chunk + 1, subscription_id)

    return "Next chunk sent!"



if __name__ == '__main__':
    app.run(debug=True)
