import pymongo
import os
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.request as urllib2
from html.parser import HTMLParser
from google_images_download import google_images_download

import logging as log

class MongoController():

    def __init__(self):
        # intantiate google image client gic object
        self.gic = google_images_download.googleimagesdownload()
        log.basicConfig(filename="tophitslogs.log", level=log.DEBUG)

    """
    dashboard or home controller functions
    """

    def get_top_pleasant_songs(self, mongo):
        """
        fetches top 5 pleasant songs from mongodb
        """
        cursor = mongo.db.songs.find(
            {},
            {"id": 1, "youtube_id": 1, "song_title": 1, "artist_name": 1, "duration": 1, "years": 1},
        ).sort("valence", pymongo.DESCENDING).limit(5)

        # take out results from cursor
        results = [res for res in cursor]

        # check if a new song is added which doest not has its coverphoto
        # if there is no coverphoto then download it from google images
        self.check_for_coverphotos(results)
        # also check for youtube ids
        self.check_for_youtube_ids(results, mongo)

        return results

    def get_top_energetic_songs(self, mongo):
        """
        fetches top 5 energetic songs from mongodb
        """
        cursor = mongo.db.songs.find(
            {},
            {"id": 1, "youtube_id": 1, "song_title": 1, "artist_name": 1, "duration": 1, "years": 1},
        ).sort("energy", pymongo.DESCENDING).limit(5)

        # take out results from cursor
        results = [res for res in cursor]

        # check if a new song is added which doest not has its coverphoto
        # if there is no coverphoto then download it from google images
        self.check_for_coverphotos(results)
        # also check for youtube ids
        self.check_for_youtube_ids(results, mongo)

        return results

    def get_non_acoustic_songs(self, mongo):
        """
        fetches top 5 non-acoustic songs from mongodb
        """
        cursor = mongo.db.songs.find(
            {},
            {"id": 1, "youtube_id": 1, "song_title": 1, "artist_name": 1, "duration": 1, "years": 1},
        ).sort("Sound_quailty", pymongo.ASCENDING).limit(5)

        # take out results from cursor
        results = [res for res in cursor]

        # check if a new song is added which doest not has its coverphoto
        # if there is no coverphoto then download it from google images
        self.check_for_coverphotos(results)
        # also check for youtube ids
        self.check_for_youtube_ids(results, mongo)

        return results

    def get_acoustic_songs(self, mongo):
        """
        fetches top 5 acoustic songs from mongodb
        """
        cursor = mongo.db.songs.find(
            {},
            {"id": 1, "youtube_id": 1, "song_title": 1, "artist_name": 1, "duration": 1, "years": 1},
        ).sort("Sound_quailty", pymongo.DESCENDING).limit(5)

        # take out results from cursor
        results = [res for res in cursor]

        # check if a new song is added which doest not has its coverphoto
        # if there is no coverphoto then download it from google images
        self.check_for_coverphotos(results)
        # also check for youtube ids
        self.check_for_youtube_ids(results, mongo)

        return results

    def get_danceable_songs(self, mongo):
        """
        fetches top 5 danceable songs from mongodb
        """
        cursor = mongo.db.songs.find(
            {},
            {"id": 1, "youtube_id": 1, "song_title": 1, "artist_name": 1, "duration": 1, "years": 1},
        ).sort("danceability", pymongo.DESCENDING).limit(5)

        # take out results from cursor
        results = [res for res in cursor]

        # check if a new song is added which doest not has its coverphoto
        # if there is no coverphoto then download it from google images
        self.check_for_coverphotos(results)
        # also check for youtube ids
        self.check_for_youtube_ids(results, mongo)

        return results

    def get_low_tempo_songs(self, mongo):
        """
        fetches top 5 danceable songs from mongodb
        """
        cursor = mongo.db.songs.find(
            {},
            {"id": 1, "youtube_id": 1, "song_title": 1, "artist_name": 1, "duration": 1, "years": 1},
        ).sort("tempo", pymongo.ASCENDING).limit(5)

        # take out results from cursor
        results = [res for res in cursor]

        # check if a new song is added which doest not has its coverphoto
        # if there is no coverphoto then download it from google images
        self.check_for_coverphotos(results)
        # also check for youtube ids
        self.check_for_youtube_ids(results, mongo)

        return results

    def find_filtered_songs(self, mongo, energy_level, sound_quality,
                    danceability, valence, loudness, instrumentalness):
        """
        searches songs by applying specific filters and return results
        """

        cursor = mongo.db.songs.find({ '$and':[{'energy': {'$lte': energy_level}}, {'Sound_quailty': {'$lte': sound_quality}}, {'danceability': {'$lte': danceability}}, {'valence': {'$lte': valence}}]})

        filtered_songs = [res for res in cursor]
        # check for coverphotos
        self.check_for_coverphotos(filtered_songs)

        #check for check_for_youtube_ids
        self.check_for_youtube_ids(filtered_songs, mongo)

        return filtered_songs

    """
    dashboard or home controller functions end here
    """

    """
    when a user searches a song by song title controller functions
    """
    def search_song_by_title(self, song_title, mongo):
        """
        gets most suitable searched song from mongodb and return it
        """
        cursor = mongo.db.songs.find({'$text': {'$search': song_title}})
        searched_song = [res for res in cursor]
        # check song for converphoto
        self.check_for_coverphotos(searched_song)
        # check for youtube audio id
        self.check_for_youtube_ids(searched_song, mongo)

        # convert it into a singular song
        for song in searched_song:
            searched_song = song

        # find song related to this song i-e artist name
        cursor = mongo.db.songs.find({
            '$or': [
                {'artist_name': searched_song['artist_name']},
                {'key': searched_song['key']},
                {'mode': searched_song['mode']},
                {'years': searched_song['years']}
            ]
        }).limit(20)

        # store result in related songs array
        related_songs = [res for res in cursor]

        # check for songs coverphotos
        self.check_for_coverphotos(related_songs)
        # check for youtube ids
        self.check_for_youtube_ids(related_songs, mongo)

        # return both results
        return searched_song, related_songs

    def search_song_by_artist_name(self, artist_name, mongo):
        """
        gets most suitable searched song of a particular singer
        """
        cursor = mongo.db.songs.find({'$text': {'$search': artist_name}})
        searched_songs = [res for res in cursor]

        # check song for converphoto
        self.check_for_coverphotos(searched_songs)
        # check for youtube audio id
        self.check_for_youtube_ids(searched_songs, mongo)
        # check for Artists
        self.check_for_artists_photo(searched_songs)

        return searched_songs

    def search_artist(self, artist_name, mongo):
        """
        find artist profile
        """
        cursor = mongo.db.songs.find({'artist_name': artist_name})
        searched_songs = [res for res in cursor]

        # check song for converphoto
        self.check_for_coverphotos(searched_songs)
        # check for youtube audio id
        self.check_for_youtube_ids(searched_songs, mongo)
        # return both results
        return searched_songs

    def get_artists(self, mongo):
        """
        get all artists in mongodb
        """
        cursor =  mongo.db.songs.aggregate([{
        '$group': {
            '_id': "$artist_name",
            'count': {
                '$sum': 1
                }
            }},
            {'$limit': 200}
        ])
        artists = []
        for res in cursor:
            artists.append({
            'artist_name': res.get('_id'),
            'count': res.get('count')
            })

        # check for artist photos
        self.check_for_artists_photo(artists)
        # return artists
        return artists

    def check_for_coverphotos(self, results):
        """
        checks if a song contains converphoto in database
        if not than download it from googleimages
        """
        # itertate over each song of results
        log.info(str(len(results)))
        i = 0
        for idx, result in enumerate(results):
            i = i + 1
            log.info(str(i))
            # get path for coverphoto
            coverphoto = result['song_title'].replace(" ", "").replace(",", "").lower()
            coverphoto = Path("static/img/coverphotos/"+ coverphoto + ".jpg")

            # if coverphoto for that song does not exists
            if coverphoto.is_file() == False:
                # set arguments to pass to gic
                arguments = {
                "keywords": result['song_title'].replace(",", "") + " cover photo",
                "limit":1, "format": "jpg",
                "output_directory": "static/img/coverphotos"}
                # download image, it returns a dict containing photo path
                coverphoto_path = self.gic.download(arguments)
                # get path of cover photo from dict
                coverphoto_path = Path(coverphoto_path[result['song_title'].replace(",", "") + " cover photo"][0]);
                # rename file to desired name
                os.rename(coverphoto_path, coverphoto)

            # convert duration from seconds to minutes
            result['duration'] = self.humanize_time(result['duration'])[3:]


    def check_for_artists_photo(self, artists):
        """
        checks if database contains photo for an artis
        if not than download it from googleimages
        """
        # itertate over each song of results
        i = 0
        for artist in artists:
            i = i + 1
            log.info(str(i))
            # get path for coverphoto
            photopath = artist['artist_name'].replace(" ", "").lower()
            # if there exists any ',' in the path then remove it
            photopath = photopath.replace(",", "")
            photopath = Path("static/img/artistphotos/"+ photopath + ".jpg")

            # if coverphoto for that song does not exists
            if photopath.is_file() == False:
                # set arguments to pass to gic
                arguments = {
                "keywords": (artist['artist_name'].replace(",", "")) + " wallpaper",
                "limit":1, "format": "jpg",
                "output_directory": "static/img/artistphotos"}
                # download image, it returns a dict containing photo path
                artist_photo_path = self.gic.download(arguments)
                # get path of cover photo from dict
                artist_photo_path = Path(artist_photo_path[(artist['artist_name'].replace(",", "")) + " wallpaper"][0])
                # rename file to desired name
                os.rename(artist_photo_path, photopath)


    def check_for_youtube_ids(self, songs, mongo):
        """
        check for youtube songs ids if not present then fetch from youtube
        """
        for song in songs:
            if song.get('youtube_id') is None:
                self.fetch_song_youtube_id(song, mongo)


    def fetch_song_youtube_id(self, song, mongo):
        """
        fetch id from youtube
        """
        # set youtube id to None
        song['youtube_id'] = None
        textToSearch = song.get('song_title')
        log.info("Text to search " + textToSearch)

        # prepare query
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        # make an http connection over this url
        response = urllib2.urlopen(url)
        # fetch html response
        html = response.read()

        # soup = BeautifulSoup(html)
        # for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            # song_id = vid['href']
            # song['youtube_id'] = song_id[song_id.index("=") + 1: ]

        # feed this response to htmlParser
        htmlParser = MyHTMLParser()
        htmlParser.feed(str(html))
        # fetch song id
        song_id =  htmlParser.song_id
        song['youtube_id'] = song_id
        # save it into mongodb
        mongo.db.songs.update({'id': song.get('id')}, {'$set': {'youtube_id': song.get('youtube_id')}})


    def humanize_time(self, secs):
        """
        converts time into human readable format
        """
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        return '%02d:%02d:%02d' % (hours, mins, secs)


class MyHTMLParser(HTMLParser):
    """
    Defined a class to parse html file and fetch video links
    """

    # define song id to access it later
    song_id = ""
    index = 0
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, return it id exists.
               if name == "href":
                   if "/watch?v=" in value:
                       if self.index == 0:
                           self.song_id = value[value.index("=") + 1:]
                           self.index = self.index + 1
                           break
