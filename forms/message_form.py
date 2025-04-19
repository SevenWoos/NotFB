from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

# 2) Create the Send Message Form
class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
  

