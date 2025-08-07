from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Movie
from data_manager import DataManager
from services.omdb_service import fetch_movie_data
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize database
db.init_app(app)
data_manager = DataManager(db)

# Create tables
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get('name')
    if name:
        existing = User.query.filter_by(name=name).first()
        if existing:
            flash(f'User {name} already exists!', 'error')
        else:
            data_manager.create_user(name)
            flash(f'User {name} created successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies')
def user_movies(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('home'))

    movies = data_manager.get_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    if title:
        movie_data = fetch_movie_data(title)
        if movie_data:
            data_manager.add_movie(user_id, movie_data)
            flash(f'Movie {movie_data["name"]} added successfully!', 'success')
        else:
            flash('Movie not found in OMDB', 'error')
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(movie_id):
    new_title = request.form.get('new_title')
    user_id = request.form.get('user_id')

    if new_title:
        movie_data = fetch_movie_data(new_title)
        if movie_data:
            updated = data_manager.update_movie(
                movie_id,
                name=movie_data['name'],
                director=movie_data['director'],
                year=movie_data['year'],
                poster_url=movie_data['poster_url']
            )
            if updated:
                flash('Movie updated successfully!', 'success')
            else:
                flash('Movie not found', 'error')
        else:
            flash('Movie not found in OMDB', 'error')
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(movie_id):
    user_id = request.form.get('user_id')
    if data_manager.delete_movie(movie_id):
        flash('Movie deleted successfully!', 'success')
    else:
        flash('Movie not found', 'error')
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)