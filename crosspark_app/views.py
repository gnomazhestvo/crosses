from . import app, db
from . forms import CrossAddForm
from .models import Cross
from flask import render_template, flash


@app.route('/')
def index_view():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard_view():
    return render_template('leaderboard.html')

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
        return 'nice'
    return render_template('add.html')