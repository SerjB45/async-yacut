from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, SubmitField
from wtforms.validators import DataRequired


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы для загрузки',
        validators=[DataRequired(
            message='Пожалуйста, выберите хотя бы один файл для загрузки.')]
    )

    submit = SubmitField('Загрузить')
    
class ShortUrlForm(FlaskForm):
    original_link = StringField(
        'Введите URL для сокращения',
        validators=[DataRequired(message='Пожалуйста, введите URL.')]
    )
    custom_id = StringField(
        'Введите пользовательский короткий идентификатор (необязательно)'
    )
    submit = SubmitField('Сократить')    