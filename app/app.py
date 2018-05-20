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

@app.route('/artists')
def artists():
    artists = mongoc.get_artists(mongo)
    return render_template("artists.html", artists=artists)


# , method['POST']
@app.route('/search_songs', methods=['POST']) #, methods=['POST']
def handle_user_song_search():
    # get search fields from request object
    search_field_text = request.form.get('search_field')
    search_base_option = request.form.get('options')
    # search_base_option = "0"
    # search_field_text = "Rihanna"

    # fetch searched song using mongo object using depends upon option
    if search_base_option == "1": # if user searches songs using song title
        searched_song, related_songs = mongoc.search_song_by_title(search_field_text, mongo)
        return render_template("song_detail.html",
            searched_song=searched_song, related_songs=related_songs)
    elif search_base_option == "0": # else if user searches by artist
        searched_songs = mongoc.search_song_by_artist_name(search_field_text, mongo)
        for song in searched_songs:
            artist_name = song.get('artist_name')
            break
            # filters
        return render_template("user.html", searched_songs=searched_songs, artist_name=artist_name)
        # return render_template("artist_profile.html")


@app.route('/artists/<artist_name>')
def artist_profile(artist_name):
    searched_songs = mongoc.search_artist(artist_name, mongo)
    return render_template("user.html", searched_songs=searched_songs, artist_name=artist_name)


@app.route('/filters')
def filters():
    """
    Fetches songs by applying default filters
    """
    filtered_songs = mongoc.find_filtered_songs(mongo, 0.5, 0.5,
                    0.5, 0.5, 0.5, 0.5)
    return render_template("filters.html", searched_songs=filtered_songs)


@app.route('/search_filtered_songs', methods=['POST'])
def handle_filtering():
    #get filter form feilds
    energy_level = request.form.get('energy_level')
    energy_level_checkbox = request.form.get('energy_level_checkbox')

    sound_quality = request.form.get('sound_quality')
    sound_quality_checkbox = request.form.get('sound_quality_checkbox')

    danceability = request.form.get('danceability')
    danceability_checkbox = request.form.get('danceability_checkbox')

    valence = request.form.get('valence')
    valence_checkbox = request.form.get('valence_checkbox')

    loudness = request.form.get('loudness')
    loudness_checkbox = request.form.get('loudness_checkbox')

    instrumentalness = request.form.get('instrumentalness')
    instrumentalness_checkbox = request.form.get('instrumentalness_checkbox')

    if energy_level_checkbox is not None:
        energy_level = float(energy_level)/100
    else:
        energy_level = 1

    if sound_quality_checkbox is not None:
        sound_quality = float(sound_quality)/100
    else:
        sound_quality = 1

    if danceability_checkbox is not None:
        danceability = float(danceability)/100
    else:
        danceability = 1

    if valence_checkbox is not None:
        valence = float(valence)/100
    else:
        valence = 1

    log.info(str(energy_level) + " " + str(sound_quality) +
     "  " + str(danceability) + "  " + str(valence))
    filtered_songs = mongoc.find_filtered_songs(mongo, energy_level, sound_quality,
                    danceability, valence, loudness, instrumentalness)

    for song in filtered_songs:
        log.info(song.get('song_title'))

    return render_template("filters.html", searched_songs=filtered_songs)


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
