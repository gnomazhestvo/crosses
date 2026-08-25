import random
from . import app, db
from . forms import CrossAddForm
from .models import Cross
from flask import render_template, flash, redirect, url_for, request


@app.route('/')
def index_view():
    return render_template('index.html')


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


@app.route('/vote') # POST больше не нужен, работаем через обычные ссылки
def vote_view():
    # Получаем ID из параметров ссылки: /vote?winner_id=...&loser_id=...
    winner_id = request.args.get('winner_id', type=int)
    loser_id = request.args.get('loser_id', type=int)
    
    if winner_id and loser_id:
        winner = Cross.query.get(winner_id)
        loser = Cross.query.get(loser_id)
        
        if winner and loser:
            # Elo-расчёт
            expected_winner = 1 / (1 + 10 ** ((loser.rating - winner.rating) / 400))
            expected_loser = 1 - expected_winner
            
            K = 32  
            winner.rating += K * (1 - expected_winner)
            loser.rating += K * (0 - expected_loser)

            db.session.commit()

    # После подсчета рейтинга просто перенаправляем пользователя на игру.
    # Функция tinder_for_shoes_view сама выберет новую случайную пару из базы!
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
        )
        db.session.add(cross)
        db.session.commit()
        flash('Кроссовок добавлен')
        return redirect(url_for('add_view'))
    return render_template('add_shoe.html', form=form)
