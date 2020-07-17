import sys
# import thread
import webbrowser
import time

import SimpleHTTPServer
import urllib
import SocketServer

PORT = 80

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(urllib.urlopen(self.path), self.wfile)


def start_server():
    httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 3600), SimpleHTTPServer.SimpleHTTPRequestHandler)
    httpd.serve_forever()

thread.start_new_thread(start_server,())
url = 'http://127.0.0.1:3600'
webbrowser.open_new(url)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)