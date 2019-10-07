import Keymaster
import KeymasterLan
import time
from Server import Server
import threading
import requests
from requests.adapters import HTTPAdapter
import configparser
import sys

cfg = configparser.ConfigParser()

try:
    cfg.read('keymaker.conf')
except Exception as err:
    print('Config load error: {0}'.format(err))
    sys.exit(0)

KEYMASTER_DRIVER = cfg.get('MAIN', 'driver_type')  # Can be LAN or SERIAL
API_URL = cfg.get('MAIN', 'api_url')
POSTOMAT_NUMBER = cfg.get('MAIN', 'postomat_number')


if KEYMASTER_DRIVER == "LAN":
    ser = KeymasterLan.KeymasterLan(cfg.get('DEVICE_LAN', 'ip'), cfg.get('DEVICE_LAN', 'port'))
elif KEYMASTER_DRIVER == "SERIAL":
    ser = Keymaster.Keymaster(
        cfg.get('DEVICE_SERIAL', 'port'),
        cfg.getint('DEVICE_SERIAL', 'baudrate'),
        cfg.getint('DEVICE_SERIAL', 'timeout'),
        cfg.getint('DEVICE_SERIAL', 'stopbits'))


def server_handler():
    global cfg
    server = Server(cfg.get('SERVICE', 'hostname'), cfg.getint('SERVICE', 'port'), ser)
    server.start()


def send_status(data):
    try:
        send_data = ''
        for i in data:
            send_data += str(int(data.get(i))) + ":"
        print(send_data)

        service_api_adapter = HTTPAdapter(max_retries=3)
        session = requests.Session()
        session.mount(API_URL, service_api_adapter)
        response = session.post(API_URL, data={'locker_statuses': send_data, 'postomat_number': POSTOMAT_NUMBER}, timeout=1.5)
        if response.status_code == 200:
            print('Status sent successfully')
        print(response.content)
        print(response.status_code)
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
            ser.request_locker_status(0x03)
            time.sleep(1)
            new_state = ser.get_current_state()
            changed = False
            for i in range(0, 16):
                if current_state[i] is not new_state[i]:
                    changed = True
                current_state[i] = new_state[i]

            if changed:
                sending_thread = threading.Thread(target=send_status, args=(current_state, ))
                sending_thread.start()
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

