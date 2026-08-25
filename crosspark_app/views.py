import random
from . import app, db
from . forms import CrossAddForm
from .models import Cross
from flask import render_template, flash, redirect, url_for, request


@app.route('/')
def index_view():
    random_shoes = []
    for _ in range(len(Cross.query.all())):
        random_shoes.append(Cross.query.order_by(db.func.random()).first())
    return render_template('index.html', random_shoes = random_shoes)


@app.route('/leaderboard')
def leaderboard_view():
    shoes = Cross.query.all()
    return render_template('leaderboard.html', shoes=shoes)


@app.route('/the_game', methods=['GET', 'POST'])
def tinder_for_shoes_view():
    shoes = Cross.query.all()

    if len(shoes) < 2:
        return render_template('tinder_for_shoes.html', error = 'Добавь еще моделей')

    shoe1, shoe2 = random.sample(shoes, 2)
    return render_template('tinder_for_shoes.html', shoe1=shoe1, shoe2=shoe2)


from flask import request, redirect, url_for # убедитесь, что импортирован redirect и url_for


@app.route('/vote', methods=['POST'])
def vote_view():
    winner_id = request.form.get('winner_id')
    loser_id = request.form.get('loser_id')

    if not winner_id or not loser_id:
        flash('Ошибка голосования')
        return redirect(url_for('tinder_for_shoes_view'))
    
    winner = Cross.query.get(winner_id)
    loser = Cross.query.get(loser_id)

    if not winner or not loser:
        flash('Ошибка: модели не найдены')
        return redirect(url_for('tinder_for_shoes_view'))

    expected_winner = 1 / (1 + 10 ** ((loser.rating - winner.rating) / 400))
    expected_loser = 1 - expected_winner
    
    K = 32  
    winner.rating += round(K * (1 - expected_winner), 0)
    loser.rating += round(K * (0 - expected_loser), 0)

    db.session.commit()

    return redirect(url_for('tinder_for_shoes_view'))



@app.route('/add', methods=['GET', 'POST'])
def add_view():
    form = CrossAddForm()
    if form.validate_on_submit():
        title = form.title.data
        if Cross.query.filter_by(title=title).first() is not None:
            flash('Эта модель уже есть!')
            return render_template('add_shoe.html', form=form)
        cross = Cross(
            title=title,
            price_male=form.price_male.data,
            price_princess=form.price_princess.data,
            description=form.description.data,
            source=form.source.data,
            image_url=form.image_url.data
        )
        db.session.add(cross)
        db.session.commit()
        flash('Кроссовок добавлен')
        return redirect(url_for('add_view'))
    return render_template('add_shoe.html', form=form)
