import keyboard
import requests

qr_data = ""
url = 'http://localhost:8080/qr-data'

def on_press(event):
    global qr_data
    if event.name == "enter":
        print("QR code scanned:", qr_data)
        payload = {'data': qr_data}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        if response.ok:
            print(response.text)
        else:
            print("Error:", response.status_code)
        qr_data = ""
    else:
        qr_data += event.name

keyboard.on_press(on_press)

# This loop keeps the script running
while True:
    pass
