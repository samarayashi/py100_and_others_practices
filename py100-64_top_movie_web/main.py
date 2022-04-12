from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
import requests

MOVIE_SEARCH_URI = "https://api.themoviedb.org/3/search/movie"
MOVIE_INFO_URI = "https://api.themoviedb.org/3/movie/"
MOVIE_IMAGE_URI = "https://image.tmdb.org/t/p/w500/"
TMDB_API_KEY = "f06ed701488b0fcabb11b0fdb81839ae"

# flask config with boostrap
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# config db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# declare Movie model, use it to control table
# you need to declare it everytime, when you want to use it.
# default table name came from converted class name which following lowercase and CamelCase.
# “CamelCase” converted to “camel_case”. Set __tablename__ class attribute to override it.
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<movie {self.title}>'


# initialize table
# if table already exists it will not create
db.create_all()

# # add first data to test
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


# create WTF form
class RateMovieForm(FlaskForm):
    rating = DecimalField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()],
                          render_kw={"autofocus": True, "autocomplete": "off"})
    review = StringField(label='Your Review', render_kw={"autocomplete": "off"})
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()],
                        render_kw={"autofocus": True, "autocomplete": "off"})
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    # sort it by sqlAlchemy
    # all_movies = Movie.query.order_by(Movie.rating).all()
    # all_movies.reverse()
    all_movies = Movie.query.order_by(Movie.rating.desc()).all()
    for rank, movie in enumerate(all_movies, start=1):
        movie.ranking = rank
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        params = {"api_key": TMDB_API_KEY, "query": form.title.data}
        response = requests.get(MOVIE_SEARCH_URI, params=params)
        data = response.json()["results"]
        if not data:
            return render_template("add.html", form=form, not_found=True)
        else:
            for movie in data:
                if 'release_date' not in movie:
                    movie['release_date'] = ''
            sorted_data = sorted(data, key=lambda m: m["release_date"], reverse=True)
        return render_template("select.html", movies=sorted_data)
    return render_template("add.html", form=form, not_found=False)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get('id')
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(f"{MOVIE_INFO_URI}/{movie_api_id}", params=params)
    data = response.json()
    new_movie = Movie(
        title=data["original_title"],
        year=data["release_date"].split("-")[0],
        description=data["overview"],
        img_url=f"{MOVIE_IMAGE_URI}/{data['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("rate_movie", id=new_movie.id))


if __name__ == '__main__':
    # use_reloader will make first_data be add more than one time.(produce unique key error)
    # app.run(debug=True, use_reloader=False)
    app.run(debug=True)
