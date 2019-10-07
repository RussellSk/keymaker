from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib.parse


class ServerHandler(BaseHTTPRequestHandler):
    serial = None

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Handle GET request"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        params = urllib.parse.parse_qs(self.path[2:])
        if "locker" in params:
            locker_number = int("".join(map(str, params['locker'])))
            self.serial.open_locker(locker_number - 1)

        self.wfile.write(b'<html><body><h1>Source</h1></body></html>')

    def set_serial_driver(self, driver):
        self.serial = driver
