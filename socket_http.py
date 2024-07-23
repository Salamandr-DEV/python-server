from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

import socket
import errno

import gridfs
import urllib.parse
from pymongo import MongoClient
from commannds.GetImage import Get_Jpg, Get_Png, Get_Ico
from commannds.GetMusic import Get_Music
from commannds.GetFilm import Get_Film, Get_Info_Film
from commannds.GetFilms import Get_Films, Get_page_Films
from commannds.GetCss import Get_Css
from commannds.GetJs import Get_Js
from commannds.GetHtml import Get_index, Get_Html
from commannds.GetFilename import Get_filename

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)
        print(parsed)

        if parsed.path == "/":
            Get_index(self, self.address_string())

        elif parsed.path[parsed.path.rfind('.') + 1:] == "html":
            Get_Html(self, parsed.path[parsed.path.rfind('/') + 1:], self.address_string())

        elif parsed.path[parsed.path.rfind('.') + 1:] == "css":
            Get_Css(self, parsed.path[parsed.path.rfind('/') + 1:])

        elif parsed.path[parsed.path.rfind('.') + 1:] == "js":
            Get_Js(self, parsed.path[parsed.path.rfind('/') + 1:])

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

        elif parsed.path == "/film":
            name = urllib.parse.unquote(parsed.query)
            Get_Film(self, name, db)

        elif parsed.path == "/info_film":
            name = urllib.parse.unquote(parsed.query)
            Get_Info_Film(self, name, db)

        elif parsed.path == "/films":
            name = urllib.parse.unquote(parsed.query)
            # if(name == ""):
            #     Get_page_Films(self, db)
            # else:
            Get_Films(self, name, db)


def get_server(port=8000, next_attempts=0):
    Handler = RequestHandler

    while next_attempts >= 0:
        try:
            httpd = ThreadingHTTPServer(("", port), Handler)
            return httpd
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                next_attempts -= 1
                port += 1
            else:
                raise

def main():
    PORT = 8080
    httpd = get_server(port=PORT)

    print("socket server - serving at port", PORT)
    httpd.serve_forever()

if __name__ == "__main__" :
    client = MongoClient('mongodb://localhost:27017/')
    filename = []

    with client:
        db = client.music_db
        music = gridfs.GridFS(db)

        # add_music(music)
        # db.music.insert_many(musics)
        # blist = db.list_collection_names()

        collection = db['fs.files']

        for i in collection.find():
            filename.append(i['filename'])

    main()