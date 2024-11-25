from dotenv import load_dotenv
import os
import requests
import ctypes
import time

# I need to load it from the file so my URL isn't saved on GitHub
load_dotenv()
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

def loop():
    close = False
    while not close:

        status = requests.get("webhook_url")

        match status.json().get('content'):
            case None:
                time.sleep(2)
            case "Lock": # Locks Windows
                requests.patch("webhook_url", json=neutralStatusData)   # change the data to the default
                ctypes.windll.user32.LockWorkStation()
                print("Locked")
            case "Close": # close the Programm
                requests.patch("webhook_url", json=neutralStatusData)
                close = True
                print("Closed")

try:

    neutralStatusData = {
        "content": "No State active"
    }
    requests.patch("webhook_url", json=neutralStatusData)

    loop()

except KeyboardInterrupt as e:
    # so when you try to close the programm it doesn't spam you with errors
    print("Closing the Programm")
    time.sleep(2)
except requests.exceptions.ConnectionError as e:
    # This could happen if your travel with your device but suddenly the connection cuts off (it will wait until the connection is restored)
    import socket
    print("No conntection")
    isConnected = False
    while not isConnected:
        time.sleep(300) #5 min
        try:
            socket.setdefaulttimeout(3)
            with socket.create_connection(("8.8.8.8", 53), 3):
                loop()
        except (socket.timeout, socket.error):
            isConnected = False
            continue