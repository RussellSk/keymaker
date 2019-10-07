import serial
import datetime
import time
import queue
import threading


class Keymaster:
    """"We do only what we're meant to do." ―The Keymaker"""

    ser = None

    def __init__(self, _port="COM3", _baudrate=19200, _timeout=1, _stopbits=1):
        try:
            self.command_queue = queue.Queue()
            self.ser = serial.Serial(port=_port, baudrate=_baudrate, timeout=_timeout, stopbits=_stopbits)
            self.current_state = {}
            command_thread = threading.Thread(target=self.serial_worker)
            command_thread.start()
        except serial.SerialException as err:
            print("Keymaster: open COM5 error: {0}".format(err))
            if self.ser is not None:
                if self.ser.is_open:
                    self.ser.close()

    def __del__(self):
        if self.ser is not None:
            if self.ser.is_open:
                self.ser.close()

    def serial_worker(self):
        while True:
            try:
                if not self.command_queue.empty():
                    item = self.command_queue.get()
                    print(item)
                    if item.get('command') == 'write':
                        self.ser.write(serial.to_bytes(item.get('data')))
                    if item.get('command') == 'read':
                        self.update_status(self.ser.read(9))
                    self.command_queue.task_done()
                    time.sleep(.3)
            except Exception as err:
                print('Serial worker error: {0}'.format(err))

    def update_status(self, state_bytes):
        for i in range(0, 16):
            self.current_state[i] = not ((state_bytes[4] << 8) + state_bytes[3]) & (1 << i) == 0

    def __write(self, data):
        if self.ser is None:
            self.__error("Serial connection is not established")
            return

        tmp_sum = 0x0
        for byte in data:
            tmp_sum += int(byte)
        command_sum = tmp_sum % 256

        data.append(command_sum)
        self.command_queue.put({'command': 'write', 'data': data})

    def __read(self, read_bytes):
        if self.ser is None:
            self.__error("Serial connection is not established")
            return
        self.command_queue.put({'command': 'read', 'data': []})

    def open_locker(self, number):
        print('OPEN')
        self.__write([0x02, number, 0x31, 0x03])

    def request_locker_status(self, number):
        self.__write([0x02, number, 0x30, 0x03])
        self.__read(9)

    def get_current_state(self):
        return self.current_state

    def __error(self, message):
        print("[error] " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + ": " + message)