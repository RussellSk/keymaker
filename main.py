import Keymaster
import KeymasterLan
import time
from Server import Server
import threading
import requests
from requests.adapters import HTTPAdapter

KEYMASTER_DRIVER = "LAN" #Can be LAN or SERIAL
API_URL = 'http://localhost/'

if KEYMASTER_DRIVER == "LAN":
    ser = KeymasterLan.KeymasterLan('192.168.0.178', 5000)
elif KEYMASTER_DRIVER == "SERIAL":
    ser = Keymaster.Keymaster()


def server_handler():
    server = Server('localhost', 80, ser)
    server.start()


def send_status(data):
    try:
        send_data = ''
        for i in data:
            send_data += str(i) + ":" + str(int(data.get(i))) + "::"
        print(send_data)

        service_api_adapter = HTTPAdapter(max_retries=3)
        session = requests.Session()
        session.mount(API_URL, service_api_adapter)
        response = session.put(API_URL, data={'locker_statuses': send_data}, timeout=1.5)
        if response.status_code == 200:
            print('Status sent successfully')
    except requests.exceptions.Timeout as err:
        print("API error: request TIMEOUT".format(err))
    except Exception as err:
        print("API error: {0}".format(err))


def status_handler():
    current_state = {}

    for i in range(0, 16):
        current_state[i] = False

    while True:
        try:
            time.sleep(.07)
            state_bytes = ser.getLockerStatus(0x03)
            changed = False
            for i in range(0, 16):
                state = not ((state_bytes[4] << 8) + state_bytes[3]) & (1 << i) == 0
                if current_state[i] is not state:
                    changed = True
                current_state[i] = state
                print("{0}".format(state), end=' ')

            print("")
            if changed:
                send_status(current_state)
                print("STATE CHANGED SENDING...")

        except Exception as err:
            print("Status Handler Error {0}".format(err))


if __name__ == "__main__":
    print("Post machine Driver v0.1")

    server_thread = threading.Thread(target=server_handler)
    server_thread.start()

    status_thread = threading.Thread(target=status_handler)
    status_thread.start()

    print("Server started!")

