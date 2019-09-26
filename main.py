import Keymaster
import time
from Server import Server
import threading

ser = Keymaster.Keymaster()


def server_handler():
    server = Server('localhost', 80, ser)
    server.start()


def status_handler():
    current_state = {}

    for i in range(0, 15):
        current_state[i] = 0

    while True:
        time.sleep(.2)
        print("Keymaster get status...")
        for i in range(0, 15):
            state = ser.getLockerStatus(i)
            if current_state[i] != state:
                print("Different state")
                #Send Data to IP

            current_state[i] = state


if __name__ == "__main__":
    print("Post machine Driver v0.1")

    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    status_thread = threading.Thread(target=status_handler)
    #status_thread.start()

    print("Server started!")

