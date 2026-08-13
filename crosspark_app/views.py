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

@app.route('/add')
def add_view():
    return render_template('add.html')

@app.route('/changeminder', methods=['GET', 'POST'])
def changeminder_view():
    form = CrossAddForm
    if form.validate_on_submit():
        text = form.text.data
        if Cross.query.filter_by(text=text).first() is not None:
            flash('Эта модель уже есть!')
            return render_template('add.html', form=form)
        cross
    return render_template('changeminder.html')



        opinion = Opinion(
            title=form.title.data,
            text=text,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)