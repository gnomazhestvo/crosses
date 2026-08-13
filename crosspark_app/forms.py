from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class CrossAddForm(FlaskForm):
    title = StringField(
        'Введите модель обуви',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256, message='Длина не более 256 символов')
        ]
    )
    price_male = FloatField(
        'Цена (в юанях) на мужской размер',
        validators=[
            Optional()
        ]
    )
    price_princess = FloatField(
        'Цена (в юанях) на женский размер',
        validators=[
            Optional()
        ]
    )
    description = TextAreaField(
        'Описание модели / подробнее чем понравились',
        validators=[
            DataRequired(message='Обязательное поле')
        ]
    )
    source = URLField(
        'Ссылка на товар',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256, message='Длина не более 256 символов')
        ]
    )
    submit = SubmitField('Добавить')
