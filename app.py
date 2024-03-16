import logging

from datetime import datetime

from flask import Flask, request, render_template, url_for, redirect, flash
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from extensions import db
from src.main import send_email, send_email_to_user
from web.models import Lecture, LectureCategory, User, Subscription

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'WYrsO2sH^vsW4n90pf?T#mG[}^X}dC'
db.init_app(app)


logger = logging.getLogger(__name__)


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
            message = "Ești deja abonat la această lectură."
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
            db.session.flush()
            db.session.commit()
            try:
                send_email(email, current_lecture.title, 1, new_subscription.id, book_id)
            except Exception as e:
                logger.error(e)
                new_subscription.current_chunk = 0
                db.session.commit()

            # After successful subscription, redirect to index or another success page
            message = "Felicitări! Te-ai abonat la această lectură. Verifică-ți mailul atât în inbox cât și în spam. Spor la citit!"

    return render_template('lecture.html', book_id=book_id, lecture=current_lecture, message=message)


@app.route('/send_next_chunk/<int:subscription_id>', methods=['GET'])
def send_next_chunk(subscription_id):
    # Fetch the subscription from the database
    subscription = db.session.get(Subscription, subscription_id)
    lecture_categories = LectureCategory.query.all()
    category_names = {category.name: category.id for category in lecture_categories}

    genre = request.args.get('genre', default="Toate")
    if genre in category_names and genre != "Toate":
        lectures = Lecture.query.filter_by(id_category=category_names[genre]).all()
    else:
        lectures = Lecture.query.all()
        genre = "Toate"

    if not subscription:
        return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories,
                               selected_genre=genre)

    user = subscription.user
    lecture = subscription.lecture

    if not user or not lecture:
        return "User or lecture not found!", 404

    current_chunk = subscription.current_chunk

    if current_chunk >= lecture.chunks:
        return "No more chunks to send!", 400

    # Update the current_chunk in the database
    subscription.current_chunk = current_chunk + 1
    db.session.commit()

    # Send an email with the new chunk
    send_email(user.email, lecture.title, current_chunk + 1, subscription_id, lecture.id)

    # Flash a message to the user that will be displayed in a removable dialog
    flash(lecture.title + ' partea ' + str(current_chunk+1) + ' / ' + str(lecture.chunks) + ' a fost trimisă!', 'info')

    # Return the rendered index page


    return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories, selected_genre=genre)

@app.route('/cancel_subscription/<int:subscription_id>', methods=['GET'])
def cancel_subscription(subscription_id):
    # Fetch the subscription from the database
    subscription = db.session.query(Subscription).options(joinedload(Subscription.lecture)).get(subscription_id)
    lecture_categories = LectureCategory.query.all()
    category_names = {category.name: category.id for category in lecture_categories}

    genre = request.args.get('genre', default="Toate")
    if genre in category_names and genre != "Toate":
        lectures = Lecture.query.filter_by(id_category=category_names[genre]).all()
    else:
        lectures = Lecture.query.all()
        genre = "Toate"
    if not subscription:
        return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories,
                               selected_genre=genre)

    # Delete the subscription from the database
    db.session.delete(subscription)
    db.session.commit()

    # Flash a message to the user that will be displayed in a removable dialog
    flash('Subscripția ta pentru ' + subscription.lecture.title + ' a fost anulată.', 'info')

    # Return the rendered index page
    # Redirect the user to the home page or to a confirmation page
    return render_template('index.html', lectures=lectures, lecture_categories=lecture_categories, selected_genre=genre)

if __name__ == '__main__':
    app.run(debug=True)
