import http.server

import json, os, sys

from urllib.parse import urlparse

class MyHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    path = urlparse.urlparse(self.path)
    params = urlparse.parse_qs(path.query)
    if self.path == '/':
      with open('index.html', 'r') as f:
        self._send_text(f.read(), 200)
    elif self.path.startswith('/api/get_families'):
      self._send_text(json.dumps(os.listdir(params['dir'][0])), 200)
    elif self.path.startswith('/api/get_data'):
      with open(os.path.join(params['dir'][0], params['metric'][0]), 'r') as f:
        lines = f.read().split('\n')
        lines = [json.loads(line) for line in lines if len(line) > 0]
      self._send_text(json.dumps({
        "x": [l[0] for l in lines],
        "ys": [l[1:] for l in lines],
      }), 200)
    else:
      self._send_text("x", 200)

  def do_OPTIONS(self):
      self.send_response(200, "ok")
      self.send_header('Access-Control-Allow-Credentials', 'true')
      self.send_header('Access-Control-Allow-Origin', '*')
      self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
      self.send_header("Access-Control-Allow-Headers", "*")

  def four_hundred(self, msg):
    self._send_text(msg, 400)

  def two_hundred(self, msg):
    self._send_text(msg, 200)

  def _send_text(self, msg, code):
    self.send_response(code)
    self.send_header("Content-type", "text/html")
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    if type(msg) is str:
      self.wfile.write(msg.encode())
    else:
      self.wfile.write(msg)

if __name__ == "__main__":
  hostName = "localhost"
  serverPort = int(sys.argv[1])
  server = http.server.HTTPServer((hostName, serverPort), MyHandler)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass

  server.server_close()