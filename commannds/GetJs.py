def Get_Js(self, name):
    self.send_response(200)
    self.send_header('Content-type', "text/js")
    self.end_headers()
    f = open("js/" + name, "rb")
    message = f.read()
    f.close()
    self.wfile.write(message)