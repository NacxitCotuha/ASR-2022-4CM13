import http.server, ssl

if __name__ == "__main__":
    server_address = ("localhost", 4444)
    
    httpd = http.server.HTTPServer(
        server_address,
        http.server.SimpleHTTPRequestHandler,
    )
    
    httpd.socket = ssl.wrap_socket(
        sock=httpd.socket,
        server_side=True,
        certfile="Certificado_SSL/server.pem",
    )
    
    httpd.serve_forever()
