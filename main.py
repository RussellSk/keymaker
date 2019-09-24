import Keymaster
import time

if __name__ == "__main__":
    print("Post machine Driver v0.1")

    ser = Keymaster.Keymaster()
    while(1):
        print(ser.getLockerStatus(15).hex())
        time.sleep(.100)

    #ser.openLocker(15)

