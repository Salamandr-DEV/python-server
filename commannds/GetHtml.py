def Get_index(self, adress):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    print(adress)
    try:
        if str(adress) == "127.0.0.1":
            file = open("html/audio_player.html", 'rb')
        else:
            file = open("html/audio_player.html", 'rb')
    except FileNotFoundError:
        file = open("html/404.html", 'rb')

    message = file.read()
    file.close()
    self.wfile.write(message)

def Get_Html(self, name, adress):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    print(adress)
    try:
        if str(adress) == "127.0.0.1":
            file = open("html/" + name, 'rb')
        else:
            file = open("html/" + name, 'rb')
    except FileNotFoundError:
        file = open("html/404.html", 'rb')

    message = file.read()
    file.close()
    self.wfile.write(message)