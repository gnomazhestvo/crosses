from . import app, db
from . forms import CrossAddForm
from .models import Cross
from flask import render_template, flash, redirect, url_for


@app.route('/')
def index_view():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard_view():
    shoes = Cross.query.all()
    return render_template('leaderboard.html', shoes=shoes)

@app.route('/changeminder')
def changeminder_view():
    return render_template('add.html')

@app.route('/add', methods=['GET', 'POST'])
def add_view():
    form = CrossAddForm()
    if form.validate_on_submit():
        title = form.title.data
        if Cross.query.filter_by(title=title).first() is not None:
            flash('Эта модель уже есть!')
            return render_template('add.html', form=form)
        cross = Cross(
            title = title,
            price_male = form.price_male.data,
            price_princess = form.price_princess.data,
            description = form.description.data,
            source = form.source.data,
        )
        db.session.add(cross)
        db.session.commit()
        flash('Кроссовок добавлен')
        return redirect(url_for('add_view'))
    return render_template('add.html', form = form)