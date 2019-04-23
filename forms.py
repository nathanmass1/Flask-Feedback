from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField,  BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, NumberRange, URL, AnyOf, Length, DataRequired

class RegisterForm(FlaskForm):
    """Form for registering users"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[DataRequired(message="Enter a secure password")])
    email = StringField("Email", validators=[Email(message="Better luck next time")])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    is_admin = BooleanField("Is Admin")

class LoginForm(FlaskForm):
    """ Login form """

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback form"""

    title = StringField("Title", validators=[InputRequired()])    
    content = TextAreaField("Content", validators=[InputRequired()])