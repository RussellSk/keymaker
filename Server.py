from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time
from ServerHandler import ServerHandler


class Server:
    HOSTNAME = 'localhost'
    HOSTPORT = 80
    _serial_driver = None

    def __init__(self, host, port, com_driver):
        self.HOSTNAME = host
        self.HOSTPORT = port
        self._serial_driver = com_driver

    def start(self):
        serv = ThreadingHTTPServer((self.HOSTNAME, self.HOSTPORT), ServerHandler)
        print(time.asctime(), "Server Starts - %s:%s" % (self.HOSTNAME, self.HOSTPORT))

        # inject Keymaster dependency
        serv.RequestHandlerClass.set_serial_driver(serv.RequestHandlerClass, driver=self._serial_driver)

        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            pass

        serv.server_close()
        print(time.asctime(), "Server Stops - %s:%s" % (self.HOSTNAME, self.HOSTPORT))
