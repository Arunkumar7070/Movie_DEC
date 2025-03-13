from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_movie_data', methods=['POST'])
def get_movies():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        
        url = "https://movies-tv-shows-database.p.rapidapi.com/"
        querystring = {"title": movie_name}

        headers = {
            "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
            "x-rapidapi-host": "movies-tv-shows-database.p.rapidapi.com",
            "Type": "get-movies-by-title"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        try:
            imdb_id = data["movie_results"][0]["imdb_id"]
            movie_url = f"https://imdb236.p.rapidapi.com/imdb/{imdb_id}"
            
            headers_1 = {
                "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
                "x-rapidapi-host": "imdb236.p.rapidapi.com"
            }
            response_1 = requests.get(movie_url, headers=headers_1)
            data_1 = response_1.json()
            movie_name = data_1["primaryTitle"]
            start_year = data_1["startYear"]
            runtime = data_1["runtimeMinutes"]
            average_rating = data_1["averageRating"]
            director_name = data_1["directors"][0]["fullName"] if data_1["directors"] else "N/A"

        except (IndexError, KeyError):
            movie_name = start_year = runtime = average_rating = director_name = "Data not found."

    return render_template('index.html', 
                           movie_name=movie_name,
                           start_year=start_year,
                           runtime=runtime,
                           average_rating=average_rating,
                           director_name=director_name)

if __name__ == '__main__':
    app.run(debug=True, port=5555)