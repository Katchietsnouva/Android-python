from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

handler = SimpleHTTPRequestHandler
server = TCPServer(('0.0.0.0', 8000), handler)

print("Server started on http://localhost:8000")
server.serve_forever()