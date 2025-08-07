from models import db, User, Movie


class DataManager:
    def __init__(self, db):
        self.db = db

    # User CRUD operations
    def create_user(self, name):
        new_user = User(name=name)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def get_users(self):
        return User.query.order_by(User.name).all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    # Movie CRUD operations
    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).order_by(Movie.year.desc()).all()

    def add_movie(self, user_id, movie_data):
        movie = Movie(
            name=movie_data['name'],
            director=movie_data['director'],
            year=movie_data['year'],
            poster_url=movie_data['poster_url'],
            user_id=user_id
        )
        self.db.session.add(movie)
        self.db.session.commit()
        return movie

    def update_movie(self, movie_id, **kwargs):
        movie = Movie.query.get(movie_id)
        if not movie:
            return None

        for key, value in kwargs.items():
            if hasattr(movie, key):
                setattr(movie, key, value)

        self.db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False