import os
import sys
import socket

def handle_request(request, html_path, static_path):
    try:
        method, path, _ = request.split(" ", 2)
        if method != "GET":
            return "HTTP/1.1 501 Not Implemented", b"Not Implemented"

        # Determine file path
        if path == "/":
            path = "/index.html"
        file_path = os.path.join(html_path, path.lstrip("/"))

        # Check if file exists
        if not os.path.exists(file_path):
            return "HTTP/1.1 404 Not Found", b"Not Found"

        # Serve HTML file
        if file_path.endswith(".html"):
            with open(file_path, "rb") as f:
                return "HTTP/1.1 200 OK", f.read()

        # Serve static file
        elif file_path.startswith(static_path):
            with open(file_path, "rb") as f:
                return "HTTP/1.1 200 OK", f.read()
        else:
            return "HTTP/1.1 403 Forbidden", b"Forbidden"
    except Exception as e:
        print(f"Error handling request: {e}")
        return "HTTP/1.1 500 Internal Server Error", b"Internal Server Error"

def start_server(html_path, static_path, port=8080):
    try:
        # Create a socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", port))
        server_socket.listen(1)
        print(f"Server listening on port {port}...")

        # Accept incoming connections
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            request = client_socket.recv(4096).decode("utf-8")
            response_status, response_body = handle_request(request, html_path, static_path)
            client_socket.sendall((response_status + "\r\n\r\n").encode("utf-8") + response_body)
            client_socket.close()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()


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

    start_server(html_path, static_path , port)
