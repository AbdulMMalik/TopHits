# import urllib.parse
# import urllib.request as urllib2
# from bs4 import BeautifulSoup
# from html.parser import HTMLParser
#
# file = open("dd.htl", "w")
# textToSearch = 'Stuck on You'
# query = urllib.parse.quote(textToSearch)
# print(query)
# url = "https://www.youtube.com/results?search_query=" + query
# response = urllib2.urlopen(url)
# # print(response)
# html = response.read()
#
# """
# soup = BeautifulSoup(html, "lxml")
# file.write(str(soup))
# file.close()
#
# for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
#     # print ('https://www.youtube.com' + vid['href'])
#     print (vid['href'])
#     break
#
#     # print (s1[s1.index(s2) + len(s2):])
# """
#
# class MyHTMLParser(HTMLParser):
#
#     i = 0
#     h = ""
#     def handle_starttag(self, tag, attrs):
#         # Only parse the 'anchor' tag.
#         if tag == "a":
#            # Check the list of defined attributes.
#            for name, value in attrs:
#                # If href is defined, print it.
#                if name == "href":
#                    if "/watch?v=" in value:
#                        if self.i == 0:
#                            self.h = value
#                            self.i = self.i+ 1
#                        print(value)
#                        break
#
# parser = MyHTMLParser()
# print(parser.feed(str(html)))
# print(parser.h)

import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
# Add all the available extractors
ydl.add_default_info_extractors()

result = ydl.extract_info('http://www.youtube.com/watch?v=Bg59q4puhmg'
,   download=False # We just want to extract the info
  )

if 'entries' in result:
  # Can be a playlist or a list of videos
 Video = result ['entries'] [0]
else:
  # Just a video
  video = result

print("Overe here")
for format in video['formats']:
    if format['ext'] == 'm4a':
        audio_url = format['url']
        print(audio_url)
