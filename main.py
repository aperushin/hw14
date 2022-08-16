from flask import Flask, jsonify, abort, request
from utils import (
    search_by_title, search_from_year_to_year, search_by_rating,
    search_by_genre, search_recent_by_genre, get_paired_actors_movie_count
)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.get('/movie/<title>')
def movie_title(title):
    movie_data = search_by_title(title)
    return jsonify(movie_data)


@app.get('/movie/<int:start_year>/to/<int:end_year>')
def movies_by_years(start_year, end_year):
    movies_data = search_from_year_to_year(start_year, end_year)
    return jsonify(movies_data)


@app.get('/rating/<rating>')
def movies_by_rating(rating):
    try:
        movies_data = search_by_rating(rating)
    except ValueError:
        return abort(404)

    return jsonify(movies_data)


@app.get('/genre/<genre>')
def movies_by_genre(genre):
    show_type = request.args.get('type')
    year = request.args.get('year')

    movies_list = search_by_genre(genre, show_type=show_type, year=year)

    return jsonify(movies_list)


@app.get('/genre/<genre>/recent')
def recent_movies_by_genre(genre):
    movies_data = search_recent_by_genre(genre)

    if movies_data is None:
        return abort(404)

    return jsonify(movies_data)


@app.get('/paired_actors')
def paired_actors():
    # /paired_actors?actor_one=Jack%20Black&actor_two=Dustin%20Hoffman
    actor_one = request.args.get('actor_one')
    actor_two = request.args.get('actor_two')

    if not actor_one or not actor_two:
        return abort(404)

    movie_count = get_paired_actors_movie_count(actor_one, actor_two)

    return str(movie_count)


if __name__ == '__main__':
    app.run()
