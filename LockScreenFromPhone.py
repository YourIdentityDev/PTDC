from dotenv import load_dotenv
import os
import requests
import ctypes
import time

#import socket      # this will be loaded when there is no internet connection


if os.path.exists("DcWebhook.env"):
    # I need to load it from the file so my URL isn't saved on GitHub
    load_dotenv("DcWebhook.env")
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
else:
    # The File will be created and the user input will be checked if the URL ist not right
    webhook_url = input("\"DcWebhook.env\" could not be found\nCreating new file\nInput Discord Webhook URL with the message id: ")
    if "https://disocrd.com/api/webhooks/" not in webhook_url and "/messages/" not in webhook_url:
        correctInput = False
        while not correctInput:
            # Looping as long the user gives an false input
            print("Input is not correct\nTry again\n\n")
            webhook_url = input("\"DcWebhook.env\" could not be found\nCreating new file\nInput Discord Webhook URL with the message id: ")
            if "https://disocrd.com/api/webhooks/" in webhook_url and "/messages/" in webhook_url:
                correctInput = True
    fileData = f"""#This should be the URL to the message send from the Webhook
#This message should only be used for that
DISCORD_WEBHOOK_URL={webhook_url}"""
    with open("DcWebhook.env", "w") as file:
        file.write(fileData)

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
            with socket.create_connection(("8.8.8.8", 53), 3): #pings google server to check if there is an active connection
                loop(webhook_url)
        except (socket.timeout, socket.error):
            isConnected = False
            continue