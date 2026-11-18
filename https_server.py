import ssl
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
BASE = Path(__file__).resolve().parent
SITE = BASE / ""
CERT = BASE / "cert.pem"
KEY = BASE / "key.pem"
if not SITE.is_dir():
    raise SystemExit("Missing site/ folder")
if not (CERT.is_file() and KEY.is_file()):
    raise SystemExit("Generate cert.pem and key.pem first")
handler = partial(SimpleHTTPRequestHandler, directory=str(SITE))
server = ThreadingHTTPServer(("0.0.0.0", 8443), handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_cert_chain(certfile=str(CERT), keyfile=str(KEY))
server.socket = context.wrap_socket(server.socket, server_side=True)
print("HTTPS running: https://localhost:8443/")
print("Serving ONLY site/ - press Ctrl+C to stop")
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Stopping HTTPS server")
finally:
    server.server_close()