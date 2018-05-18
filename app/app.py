from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
import youtube_dl
from controllers.mongoc import MongoController

import logging as log

app = Flask(__name__)
# configuration for monogo database server
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT']='27017'
app.config['MONGO_DBNAME']="TopHits"

# logs file
log.basicConfig(filename="tophitslogs.log", level=log.DEBUG)

# connecting to mongodb
mongo = PyMongo(app,config_prefix='MONGO')
# get an object of MongoController
mongoc = MongoController()

@app.route('/')
def home():
    # get data from mongodb for home page using monog controller
    top_pleasant_songs = mongoc.get_top_pleasant_songs(mongo)
    top_energetic_songs = mongoc.get_top_energetic_songs(mongo)
    non_acoustic_songs = mongoc.get_non_acoustic_songs(mongo)
    acoustic_songs = mongoc.get_acoustic_songs(mongo)
    danceable_songs = mongoc.get_danceable_songs(mongo)
    low_tempo_songs = mongoc.get_low_tempo_songs(mongo)

    # return rendered template
    return render_template("dashboard.html", top_pleasant_songs=top_pleasant_songs,
                top_energetic_songs=top_energetic_songs,
                non_acoustic_songs=non_acoustic_songs,
                acoustic_songs=acoustic_songs,
                danceable_songs=danceable_songs,
                low_tempo_songs=low_tempo_songs)


# , method['POST']
@app.route('/search_songs')
def handle_user_song_search():
    # get search fields from request object
    # search_field_text = request.form.get('search_field')
    # search_base_option = request.form.get('options')

    search_base_option = "1"
    search_field_text = "Stuck on You"

    # fetch searched song using mongo object using depends upon option
    if search_base_option == "1": # if user searches songs using song title
        searched_song, related_songs = mongoc.search_song_by_title(search_field_text, mongo)
        return render_template("song_detail.html",
            searched_song=searched_song, related_songs=related_songs)
    elif search_base_option == "0": # else if user searches by artist
        log.info("Came in else condition")


@app.route('/song/tophits/<song_id>/<song_title>')
def play_song(song_id, song_title):
    """
    fetches song url and plays it by rendering playsong template
    """
    audio_url = get_song_url(song_id)
    return render_template("play_song.html", audio_url=audio_url, song_title=song_title)



def get_song_url(song_id):
    """
    fetches song url based on youtube id
    """
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    # Add all the available extractors
    ydl.add_default_info_extractors()
    result = ydl.extract_info('http://www.youtube.com/watch?v=' + song_id,
        # We just want to extract the info
        download=False )
    if 'entries' in result:
        # Can be a playlist or a list of videos
        Video = result ['entries'][0]
    else:
        # Just a video
        video = result

    for format in video['formats']:
        if format['ext'] == 'm4a':
            audio_url = format['url']
            log.info(audio_url)
            return audio_url


if __name__ == '__main__':
    app.run(debug = True)
