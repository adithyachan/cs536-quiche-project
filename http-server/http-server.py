import http.server
import socketserver
import ssl

PORT = 4433

Handler = http.server.SimpleHTTPRequestHandler

CERT_FILE = "/mnt/http-server/cert.crt"  # Path to your certificate file
KEY_FILE = "/mnt/http-server/cert.key"   # Path to your private key file

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
