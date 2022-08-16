import sqlite3


def execute_query(query: str) -> list:
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        result = cursor.execute(query).fetchall()
    return result


def search_by_title(title: str) -> dict:
    """Шаг 1"""
    query = f'''
            SELECT title, country, max(release_year), listed_in, description
            FROM netflix
            WHERE title = '{title}'
        '''

    search_results = execute_query(query)
    title, country, release_year, genre, description = search_results[0]

    result = {
        "title": title,
        "country": country,
        "release_year": release_year,
        "genre": genre,
        "description": description
    }
    return result


def search_from_year_to_year(start_year: int, end_year: int):
    """Шаг 2"""
    query = f'''
            SELECT title, release_year FROM netflix
            WHERE release_year BETWEEN {start_year} AND {end_year}
            LIMIT 100
        '''

    search_results = execute_query(query)

    result = []

    for title, release_year in search_results:
        result.append({'title': title, 'release_year': release_year})

    return result


def search_by_rating(rating: str) -> list[dict]:
    """Шаг 3"""
    ratings = {
        'children': ['"G"'],
        'family': ['"G"', '"PG"', '"PG-13"'],
        'adult': ['"R"', '"NC-17"']
    }

    if rating.lower() not in ratings:
        raise ValueError('Invalid rating')

    rating_string = ', '.join(ratings[rating.lower()])

    query = f'''
            SELECT title, release_year FROM netflix
            WHERE rating IN ({rating_string})
            LIMIT 100
        '''

    search_results = execute_query(query)

    result = []

    for title, release_year in search_results:
        result.append({'title': title, 'release_year': release_year})

    return result


def search_by_genre(genre: str, show_type: str = None, year: int = None) -> list:
    """Шаг 6"""
    query = f'''
                SELECT title FROM netflix
                WHERE listed_in LIKE '%{genre}%'
            '''

    if show_type:
        query += f"AND type = '{show_type}'\n"
    if year:
        query += f"AND release_year = {year}\n"

    search_results = execute_query(query)

    return [row[0] for row in search_results]


def search_recent_by_genre(genre: str) -> list[dict] | None:
    """Шаг 4"""
    query = f'''
            SELECT title, description FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY date_added DESC
            LIMIT 10
        '''

    search_results = execute_query(query)

    if not search_results:
        return None

    result = []

    for title, description in search_results:
        result.append({'title': title, 'description': description})

    return result


def get_paired_actors_movie_count(actor_one: str, actor_two: str) -> int:
    """Шаг 5"""
    query = f'''SELECT "cast" FROM netflix'''

    search_results = execute_query(query)
    result = 0

    for row in search_results:
        if actor_one in row[0] and actor_two in row[0]:
            result += 1

    return result
