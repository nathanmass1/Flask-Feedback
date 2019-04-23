from flask import Flask, request, jsonify, render_template, session, redirect, flash
from models import User, Feedback, db, connect_db
from forms import RegisterForm, LoginForm, FeedbackForm
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_redirect():

    return redirect("/register")


@app.route('/register', methods=["GET", "POST"])
def get_register():
    """Register form; handle adding."""

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        is_admin = form.is_admin.data

        user = User.register(username=username,
                             password=password, email=email, first_name=first_name, last_name=last_name, is_admin=is_admin)

        db.session.add(user)
        db.session.commit()
        # flash(f'You just added {user.username}')
        return redirect("/")

    else:
        return render_template(
            "register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route("/users/<username>")
def show_user_profile(username):
    """Go to user profile page"""

    user = User.query.get(username)
    session_user = User.query.get(session["username"])

    if not user:
        return render_template("errorpage.html")
    print("LOOK AT ME:", session_user.is_admin)
    if "username" not in session:
        flash("You better login!")
        return redirect("/")
    elif session["username"] != user.username and not session_user.is_admin:
        flash("No peeking")
        return redirect("/login")
    else:
        return render_template("profile.html", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    user = User.query.get_or_404(username)
    session_user = User.query.get(session["username"])

    if session["username"] == user.username or session_user.is_admin:
        db.session.delete(user)
        db.session.commit()

        return redirect("/")

    else:
        flash(f"You can't delete that {username}")
        return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_user_feedback(username):

    form = FeedbackForm()
    user = User.query.get_or_404(username)
    session_user = User.query.get(session["username"])

    if "username" not in session:
        flash("You better login!")
        return redirect("/")
    if session["username"] != username and not session_user.is_admin:
        flash("Must be logged in to see form")
        return redirect("/")

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title,
                            content=content, username=session["username"])

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add_feedback.html", form=form)


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_user_feedback(feedback_id):

    userperson = Feedback.query.get(feedback_id)
    username = userperson.username
    session_user = User.query.get(session["username"])

    print(username)
    form = FeedbackForm(obj=userperson)

    if "username" not in session:
        flash("You better login!")
        return redirect("/")
    if session["username"] != username and not session_user.user.is_admin:
        flash("Must be logged in to see form")
        return redirect("/")

    if form.validate_on_submit():
        feedback = Feedback.query.get(feedback_id)

        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add_feedback.html", form=form)


@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    userperson = Feedback.query.get(feedback_id)
    username = userperson.username
    session_user = User.query.get(session["username"])

    if session["username"] == username or session_user.is_admin:
        db.session.delete(userperson)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        flash(f"You can't delete that {username}")
        return redirect("/login")


@app.route("/secret")
def show_secret():
    """Secret result"""

    if "username" not in session:
        flash("You better login!")
        return redirect("/")
    else:
        return render_template("secret.html")


@app.route("/logout")
def logout():
    session.pop("username")

    return redirect("/")
