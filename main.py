from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import random
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

# File to store remaining movies
# Vercel serverless has a read-only filesystem except /tmp/
if os.environ.get('VERCEL'):
    MOVIES_FILE = '/tmp/movies.json'
else:
    MOVIES_FILE = os.environ.get('MOVIES_FILE', 'movies.json')



INITIAL_MOVIES = [
    # 1980s Classics
    "Sholay",
    "Amar Akbar Anthony",
    "Mr. India",
    "Qayamat Se Qayamat Tak",
    "Tezaab",
    "Ram Lakhan",
    "Satte Pe Satta",
    "Disco Dancer",
    "Karz",
    "Chashme Buddoor",

    # 1990s Blockbusters
    "Dilwale Dulhania Le Jayenge",
    "Kuch Kuch Hota Hai",
    "Kabhi Khushi Kabhie Gham",
    "Hum Aapke Hain Koun",
    "Hum Saath Saath Hain",
    "Raja Hindustani",
    "Border",
    "Baazigar",
    "Aankhen",
    "Andaz Apna Apna",
    "Jo Jeeta Wohi Sikandar",
    "Ghatak",
    "Ghayal",
    "Dil To Pagal Hai",
    "Rangeela",
    "Sarfarosh",
    "Agneepath (1990)",
    "Haseena Maan Jaayegi",

    # Early 2000s
    "Lagaan",
    "Dil Chahta Hai",
    "Kabhi Alvida Naa Kehna",
    "Swades",
    "Kal Ho Naa Ho",
    "Munna Bhai M.B.B.S.",
    "Lage Raho Munna Bhai",
    "Hera Pheri",
    "Phir Hera Pheri",
    "Koi Mil Gaya",
    "Krrish",
    "Jodhaa Akbar",
    "Hum Dil De Chuke Sanam",
    "Devdas",
    "Gadar",
    "Veer-Zaara",
    "Chak De! India",
    "Rang De Basanti",
    "Black",
    "Omkara",
    "Guru",

    # 2010s Major Hits
    "3 Idiots",
    "Dangal",
    "PK",
    "Bajrangi Bhaijaan",
    "Zindagi Na Milegi Dobara",
    "Barfi!",
    "Yeh Jawaani Hai Deewani",
    "Jab We Met",
    "Bhaag Milkha Bhaag",
    "Queen",
    "Aashiqui 2",
    "Haider",
    "Stree",
    "Badhaai Ho",
    "Padmaavat",
    "Bajirao Mastani",
    "Sultan",
    "Raazi",
    "Drishyam",
    "Uri: The Surgical Strike",
    "Gully Boy",
    "Kabir Singh",
    "Rockstar",
    "Tamasha",
    "Holiday",
    "Airlift",
    "Special 26",
    "Baby",

    # 2015–2020 Strong Titles
    "Tanu Weds Manu",
    "Tanu Weds Manu Returns",
    "Dhoom",
    "Dhoom 2",
    "Dhoom 3",
    "Bang Bang",
    "Singham",
    "Simmba",
    "Ek Tha Tiger",
    "Tiger Zinda Hai",
    "War",

    # Recent (2020–2024)
    "Pathaan",
    "Jawan",
    "Gadar 2",
    "Sooryavanshi",
    "Article 15",
    "Drishyam 2",
    "OMG 2",
    "12th Fail",
    "RRR (Hindi Dubbed)",
    "Bahubali",
    "Bahubali 2"
]

def load_movies():
    """Load movies from file, or initialize if file doesn't exist"""
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, 'r') as f:
            return json.load(f)
    else:
        # Initialize with full list
        save_movies(INITIAL_MOVIES.copy())
        return INITIAL_MOVIES.copy()

def save_movies(movies):
    """Save movies to file"""
    with open(MOVIES_FILE, 'w') as f:
        json.dump(movies, f)

@app.route('/')
def index():
    """Serve the QR code page"""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/movie')
def movie_page():
    """Serve the movie display page"""
    return send_from_directory(BASE_DIR, 'movie.html')

@app.route('/logo.png')
def logo():
    """Serve the logo image"""
    return send_from_directory(BASE_DIR, 'logo.png')

@app.route('/api/movie', methods=['GET'])
def get_random_movie():
    """Get a random movie and remove it from the list"""
    movies = load_movies()
    
    if not movies:
        return jsonify({
            'error': 'No movies left',
            'message': 'All movies have been shown!'
        }), 404
    
    # Pick a random movie
    random_movie = random.choice(movies)
    
    # Remove it from the list
    movies.remove(random_movie)
    
    # Save updated list
    save_movies(movies)
    
    return jsonify({
        'movie': random_movie,
        'remaining': len(movies)
    })

@app.route('/api/reset', methods=['POST'])
def reset_movies():
    """Reset the movie list (for testing purposes)"""
    save_movies(INITIAL_MOVIES.copy())
    return jsonify({
        'message': 'Movie list reset successfully',
        'total': len(INITIAL_MOVIES)
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the current status of movies"""
    movies = load_movies()
    return jsonify({
        'remaining': len(movies),
        'total': len(INITIAL_MOVIES),
        'shown': len(INITIAL_MOVIES) - len(movies)
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 8080 (GCP Cloud Run)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)