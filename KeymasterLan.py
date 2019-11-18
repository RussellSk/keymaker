import socket
import time
import queue
import threading
import os


class KeymasterLan:
    client = None

    def __init__(self, addr, port):
        self.address = addr
        self.port = port
        self.connect()
        self.current_state = {}
        self.command_queue = queue.Queue()
        lan_worker = threading.Thread(target=self.lan_worker)
        lan_worker.start()

    def __del__(self):
        self.disconnect()

    def connect(self):
        for i in range(5):
            try:
                self.disconnect()
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(1)
                self.client.connect((self.address, self.port))
                break
            except Exception as err:
                print("Connection error: {0}".format(err))
            if i == 4:
                os._exit(1)

    def disconnect(self):
        if self.client is not None:
            self.client.close()
            self.client = None

    def lan_worker(self):
        while True:
            try:
                if not self.command_queue.empty():
                    item = self.command_queue.get()
                    if item.get('command') == 'write':
                        self.client.send(item.get('data'))
                    if item.get('command') == 'read':
                        self.update_status(self.client.recv(9))
                    self.command_queue.task_done()
                    time.sleep(.3)
            except Exception as err:
                print('Serial worker error: {0}'.format(err))

    def update_status(self, state_bytes):
        for i in range(0, 16):
            self.current_state[i] = not ((state_bytes[4] << 8) + state_bytes[3]) & (1 << i) == 0

    def __write(self, data):
        if self.client is None:
            self.connect()

        tmp_sum = 0x0
        for byte in data:
            tmp_sum += int(byte)
        command_sum = tmp_sum % 256

        data.append(command_sum)
        self.command_queue.put({'command': 'write', 'data': bytes(data)})

    def __read(self, read_bytes):
        if self.client is None:
            self.connect()

        self.command_queue.put({'command': 'read', 'data': []})

    def open_locker(self, number):
        self.__write([0x02, number, 0x31, 0x03])

    def request_locker_status(self, number):
        self.__write([0x02, number, 0x30, 0x03])
        self.__read(9)

    def get_current_state(self):
        return self.current_state


if __name__ == '__main__':
    print("Keymaker LAN")
    ser = KeymasterLan('192.168.0.178', 5000)
    #ser.openLocker(15)

    while True:
        status = ser.getLockerStatus(15)
        print(status[4])
        print(status)
        time.sleep(1)

