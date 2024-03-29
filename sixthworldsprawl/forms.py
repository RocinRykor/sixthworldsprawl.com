from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),
                                                   Length(max=30)])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     Length(min=12)])
    submit = SubmitField("Login")


class UserForm(FlaskForm):
    name = StringField("Display", validators=[InputRequired(),
                                              Length(max=30)])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     Length(min=12)])
    confirmation = PasswordField(
        "Password Confirmation",
        validators=[InputRequired(),
                    Length(min=12),
                    EqualTo("password",
                            message="Must match password")])
    is_admin = BooleanField("Admin?")
    submit = SubmitField("Sign Up")


class EditUserForm(FlaskForm):
    name = StringField("Display", validators=[InputRequired(),
                                              Length(max=30)])
    bio = TextAreaField("Bio", validators=[InputRequired(), Length(max=2048)])
    submit = SubmitField("Edit User")


class CharacterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=32)])
    bio = TextAreaField("Bio", validators=[InputRequired(), Length(max=2048)])
    race = StringField("Race", validators=[InputRequired(), Length(max=32)])
    gender = StringField("Gender", validators=[InputRequired(), Length(max=32)])
    status = StringField("Status", validators=[InputRequired(), Length(max=64)])
    portrait_id = StringField("Portrait ID", validators=[InputRequired(), Length(max=8)])
    portrait_filename = StringField("Portrait filename", validators=[InputRequired(), Length(max=64)])

    submit = SubmitField("Add Character")
