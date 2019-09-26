import socket
import time


class KeymasterLan:
    client = None

    def __init__(self, addr, port):
        self.address = addr
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(1)
        self.client.connect((self.address, self.port))

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def __write(self, data):
        if self.client is None:
            print("Socket is not established")
            return

        tmpSum = 0x0
        for byte in data:
            tmpSum += int(byte)
        sum = tmpSum % 256

        data.append(sum)

        self.client.send(bytes(data))

    def __read(self, read_bytes):
        if self.client is None:
            print("Socket is not established")
            return

        return self.client.recv(read_bytes)

    def openLocker(self, number):
        self.__write([0x02, number, 0x31, 0x03])

    def getLockerStatus(self, number):
        #print([0x02, number, 0x30, 0x03])
        self.__write([0x02, number, 0x30, 0x03])
        return self.__read(9)


if __name__ == '__main__':
    print("Keymaker LAN")
    ser = KeymasterLan('192.168.0.178', 5000)
    #ser.openLocker(15)

    while True:
        status = ser.getLockerStatus(15)
        print(status[4])
        print(status)
        time.sleep(1)

