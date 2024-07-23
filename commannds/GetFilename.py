import random

def Get_filename(self, filename):
    self.send_response(200)
    fileName = random.choice(filename)
    self.send_header('Content-type', "text/plain")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    print(fileName)
    self.wfile.write(bytes(fileName, "utf8"))
