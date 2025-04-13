from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length
from flask_wtf.file import FileField, FileAllowed

class ProfileEditForm(FlaskForm):
    bio = StringField('Bio', validators=[Length(max=500)])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')
