
def Get_Jpg(self, name):
    self.send_response(200)
    self.send_header('Content-type', "image/jpeg")
    self.end_headers()
    f = open("image_element/" + name, "rb")
    message = f.read()
    f.close()
    self.wfile.write(message)

def Get_Png(self, name):
    self.send_response(200)
    self.send_header('Content-type', "image/png")
    self.end_headers()
    f = open("image_element/" + name, "rb")
    message = f.read()
    f.close()
    self.wfile.write(message)

def Get_Ico(self, name):
    self.send_response(200)
    self.send_header('Content-type', "image/vnd.microsoft.icon")
    self.end_headers()
    f = open("image_element/" + name, "rb")
    message = f.read()
    f.close()
    self.wfile.write(message)
