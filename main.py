import Keymaster
import KeymasterLan
import time
from Server import Server
import threading

KEYMASTER_DRIVER = "LAN" #Can be LAN or SERIAL

if KEYMASTER_DRIVER == "LAN":
    ser = KeymasterLan.KeymasterLan('192.168.0.178', 5000)
elif KEYMASTER_DRIVER == "SERIAL":
    ser = Keymaster.Keymaster()


def server_handler():
    server = Server('localhost', 80, ser)
    server.start()


def status_handler():
    current_state = {}

    for i in range(0, 16):
        current_state[i] = 0

    while True:
        try:
            time.sleep(.1)
            state_bytes = ser.getLockerStatus(0x03)
            changed = False
            for i in range(0, 16):
                state = not ((state_bytes[4] << 8) + state_bytes[3]) & (1 << i) == 0
                print("{0}".format(state), end=' ')

            print("")

        except Exception as err:
            print("Status Handler Error {0}".format(err))


if __name__ == "__main__":
    print("Post machine Driver v0.1")

    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    status_thread = threading.Thread(target=status_handler)
    status_thread.start()

    print("Server started!")

