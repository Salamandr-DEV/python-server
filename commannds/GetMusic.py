import gridfs

def Get_Music(self, name, db):
    self.send_response(200)

    out, content = load_binary(name, db)

    self.send_header('Content-type', out.contentType)
    self.send_header('Content-Length', out.length)
    self.send_header('Access-Control-Allow-Origin:', "*")
    self.send_header('accept-ranges', "bytes")
    self.end_headers()

    self.wfile.write(content)

def load_binary(name, db):
    fs = gridfs.GridFSBucket(db)
    grid_out = fs.open_download_stream_by_name(filename=name)
    contents = grid_out.read(grid_out.length)
    return grid_out, contents