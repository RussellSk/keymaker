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
            print("Keymaster get status...")
            for i in range(0, 16):
                state = ser.getLockerStatus(i)
                print("State of: {0} is {1}".format(i, state))
                state = state[4]

                if current_state[i] != state:
                    print("Different state")
                    #Send Data to IP

                time.sleep(.1)

                current_state[i] = state
        except Exception as err:
            print("Status Handler Error {0}".format(err))


if __name__ == "__main__":
    print("Post machine Driver v0.1")

    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    status_thread = threading.Thread(target=status_handler)
    status_thread.start()

    print("Server started!")

