from dotenv import load_dotenv
import os
import requests
import ctypes
import time

# I need to load it from the file so my URL isn't saved on GitHub
load_dotenv("DcWebhook.env")
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

def loop(webhook_url):
    close = False
    while not close:

        status = requests.get(webhook_url)

        jsonContent = status.json().get('content')

        if "No State active" in jsonContent:
            time.sleep(2)
        elif "Lock" in jsonContent:
            requests.patch(webhook_url, json=neutralStatusData)  # change the data to the default
            ctypes.windll.user32.LockWorkStation()
            print("Locked")
        elif "Close" in jsonContent:
            requests.patch(webhook_url, json=neutralStatusData)
            close = True
            print("Closed")
        else:
            print("The Webhook did not respond.")

try:

    neutralStatusData = {
        "content": "No State active"
    }
    requests.patch(webhook_url, json=neutralStatusData)

    loop(webhook_url)

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
                loop(webhook_url)
        except (socket.timeout, socket.error):
            isConnected = False
            continue