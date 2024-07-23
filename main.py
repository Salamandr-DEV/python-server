from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient

import os
import base64
import gridfs
import random
import urllib.parse

from commannds.GetImage import Get_Jpg, Get_Png, Get_Ico
from commannds.GetMusic import Get_Music
from commannds.GetCss import Get_Css
from commannds.GetHtml import Get_index
from commannds.GetFilename import Get_filename

PORT = 8080

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)
        print(parsed)

        if parsed.path == "/":
            Get_index(self, self.address_string())

        elif parsed.path[parsed.path.rfind('.') + 1:] == "css":
            Get_Css(self, parsed.path[parsed.path.rfind('/') + 1:])

        elif parsed.path[parsed.path.rfind('.') + 1:] == "jpg":
            Get_Jpg(self, parsed.path[parsed.path.rfind('/') + 1:])

        elif parsed.path[parsed.path.rfind('.') + 1:] == "png":
            Get_Png(self, parsed.path[parsed.path.rfind('/') + 1:])

        elif parsed.path[parsed.path.rfind('.') + 1:] == "ico":
            Get_Ico(self, parsed.path[parsed.path.rfind('/') + 1:])

        elif parsed.path == "/music":
            name = urllib.parse.unquote(parsed.query)
            Get_Music(self, name, db)

        elif self.path == "/filename":
            Get_filename(self, filename)


if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    filename = []

    with client:
        db = client.music_db
        music = gridfs.GridFS(db)

        #add_music(music)
        #db.music.insert_many(musics)
        #blist = db.list_collection_names()

        collection = db['fs.files']

        for i in collection.find():
            filename.append(i['filename'])

        # for i in range(len(filename)):
        #     print(filename[i])

    serv = HTTPServer(("", PORT), HttpProcessor)
    print("server is run on port " + str(PORT))
    serv.serve_forever()