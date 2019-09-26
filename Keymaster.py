import serial
import datetime


class Keymaster:
    """"We do only what we're meant to do." ―The Keymaker"""

    ser = None

    def __init__(self, _port="COM5", _baudrate=19200, _timeout=1, _stopbits=1):
        try:
            self.ser = serial.Serial(port=_port, baudrate=_baudrate, timeout=_timeout, stopbits=_stopbits)
        except serial.SerialException as err:
            print("Keymaster: open COM5 error: {0}".format(err))
            if self.ser is not None:
                if self.ser.is_open:
                    self.ser.close()

    def __del__(self):
        if self.ser is not None:
            if self.ser.is_open:
                self.ser.close()

    def __write(self, data):
        if self.ser is None:
            self.__error("Serial connection is not established")
            return

        tmpSum = 0x0
        for byte in data:
            tmpSum += int(byte)
        sum = tmpSum % 256

        data.append(sum)

        print(data)
        self.ser.write(serial.to_bytes(data))

    def __read(self, read_bytes):
        if self.ser is None:
            self.__error("Serial connection is not established")
            return

        return self.ser.read(read_bytes)

    def openLocker(self, number):
        self.__write([0x02, number, 0x31, 0x03])

    def getLockerStatus(self, number):
        self.__write([0x02, number, 0x30, 0x03])
        return self.__read(9)



    def __error(self, message):
        print("[error] " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + ": " + message)