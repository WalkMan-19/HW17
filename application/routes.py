from application.models import db, Movie, Director, Genre
from application.schema import MovieSchema, DirectorSchema, GenreSchema
from flask_restx import Resource
from flask import current_app as app, request

api = app.config['api']

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# ----------movie_ns----------
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies = db.session.query(Movie)
        req_arg = request.args

        director_id = req_arg.get('director_id')
        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)
        genre_id = req_arg.get('genre_id')
        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)

        movies = movies.all()
        return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

        return "", 201


@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):

    def get(self, movie_id: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
            return movie_schema.dump(movie), 200
        except Exception:
            return "", 404

    def put(self, movie_id: int):
        movie = db.session.query(Movie).get(movie_id)
        req_json = request.json

        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')

        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, movie_id: int):
        movie = db.session.query(Movie).get(movie_id)

        db.session.delete(movie)
        db.session.commit()

        return "", 204


# ----------director_ns----------
@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(Director)
        return directors_schema.dump(directors), 200


@director_ns.route('/<int:director_id>')
class DirectorView(Resource):
    def get(self, director_id: int):
        try:
            director = db.session.query(Director).filter(Director.id == director_id).one()
            return director_schema.dump(director), 200
        except Exception:
            return "", 404


# ----------genre_ns----------
@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(Genre)
        return genres_schema.dump(genres)


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    def get(self, genre_id: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
            return genre_schema.dump(genre), 200
        except Exception:
            return "", 404
