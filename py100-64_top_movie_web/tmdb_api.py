import requests


def search_movie(serach_word: str) -> list[dict]:
    movie_uri = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": "f06ed701488b0fcabb11b0fdb81839ae", "query": serach_word}
    response = requests.get(movie_uri, params=params)
    data = response.json()["results"]
    for movie in data:
        if 'release_date' not in movie:
            print(movie)
    # sorted_data = sorted(data, key=lambda m: m["release_date"], reverse=True)
    # for movie in sorted_data:
    #     print(movie["title"])
    #     print(movie['release_date'])


if __name__ == "__main__":
    search_movie("123")

