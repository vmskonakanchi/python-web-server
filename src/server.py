import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Store HTML and static file paths
    def __init__(self, *args, html_path, static_path, **kwargs):
        self.html_path = html_path
        self.static_path = static_path
        super().__init__(*args, **kwargs)

    # Serve HTML and static files
    def do_GET(self):
        url_parts = urlparse(self.path)
        file_path = url_parts.path.strip("/")
        full_path = os.path.join(self.html_path, file_path)

        # Check if requested file exists
        if os.path.exists(full_path):
            # Serve HTML file
            if full_path.endswith(".html"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
            # Serve static file
            elif os.path.exists(os.path.join(self.static_path, file_path)):
                self.send_response(200)
                self.send_header("Content-type", "text/css" if file_path.endswith(".css") else "text/javascript")
                self.end_headers()
                with open(os.path.join(self.static_path, file_path), "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "File not found")

def run_server(html_path, static_path, port=8000):
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, html_path=html_path, static_path=static_path, **kwargs))
        print(f"Server running on port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <port> <html_files_path> <static_files_path>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    html_path = sys.argv[2] if len(sys.argv) > 2 else "./html"
    static_path = sys.argv[3] if len(sys.argv) > 3 else "./static"

    if not os.path.exists(html_path):
        os.makedirs('./html')

    if not os.path.exists(static_path):
        os.makedirs('./static')

    run_server(html_path, static_path , port)
