import http.server
import ssl
import os

PAGE_FOLDER = "web"
HOST = "localhost"
PORT = 50000


def main():
    pwd = os.getcwd()
    try: 
        # Use openssl to create a self signed certificate:
        # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("Certificado_SSL/cert.pem", "Certificado_SSL/key.pem")
        print(f"Servidor {PAGE_FOLDER} en {HOST}:{PORT}")
        os.chdir(PAGE_FOLDER)
        httpd = http.server.HTTPServer((HOST, PORT), http.server.SimpleHTTPRequestHandler)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        httpd.serve_forever()
    finally:
        os.chdir(pwd)



if __name__ == "__main__":
    main()
