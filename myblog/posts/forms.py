from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug')
    content = CKEditorField('Content', validators=[DataRequired()])
    topic = SelectField('Topic', validators=[DataRequired()])
    tags = StringField("Tags")
    submit = SubmitField('Submit')
