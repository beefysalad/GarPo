from tkinter import *
from tkinter import ttk
import requests
import os
import sys
import keyboard
import pyautogui
import tkinter as tk
import sys




filename = "./image.jpg"
filepath = os.path.join(os.getcwd(), filename)
qr_data = ""


def btn_clicked():
    window.destroy()
    
def on_press2(event):
    global qr_data 
    url = 'http://localhost:8080/qr-data'
    with open('points.txt','w') as f:
        f.write(str(0))
    if event.name == 'enter':
        print("QR CODE SCANNED:",qr_data)
        payload = {'data': qr_data,'points':sys.argv[2]}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url,json=payload, headers=headers)
        if response.ok:
            window.destroy()
        else:
            print("not good",response.status_code)
        qr_data = ""
    elif len(event.name) == 1 and event.name.isalnum():
       qr_data += event.name.upper() if keyboard.is_pressed('shift') else event.name.lower()
def on_press():
    url = 'http://localhost:8080/qr-data'
    with open('points.txt', 'w') as f:
        f.write(str(0))
    qr_data=pyautogui.password("Scan your QR Code")
    print("QR CODE SCANNED:",qr_data)
    payload = {'data':qr_data,'points':sys.argv[2]}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url,json=payload,headers=headers)
    if(response.ok):
        window.destroy()
    else:
        print("NOT GOOD")
    
    
def done_clicked():
    on_press()
    #keyboard.on_press(on_press)
    #window.destroy()

def paper_button():
    print("PAPER")
    folder_name = 'paper'
    url = 'http://localhost:8080/upload?folder=' + folder_name
    files = {'image': open(filepath, 'rb')}
    response = requests.post(url, files=files)
    print(response)
    window.destroy()
    
def plastic_button():
    folder_name = 'plastic'
    url = 'http://localhost:8080/upload?folder=' + folder_name
    files = {'image': open(filepath, 'rb')}
    response = requests.post(url, files=files)
    print(response)
    window.destroy()  
    
def btn_feedback():
    feedback_window = Toplevel()
    feedback_window.title("Feedback")
    feedback_window.geometry("480x320")

    # Create a Frame widget and embed the feedback window inside it
    feedback_frame = Frame(feedback_window, width=480, height=320)
    feedback_frame.pack(fill="both", expand=True)
    feedback_window.resizable(False, False)

    # Load the feedback window content into the Frame widget
    feedback_content = Canvas(feedback_frame, width=480, height=320,bg='#292929')
    feedback_content.pack(fill="both", expand=True)

    img0 = PhotoImage(file="./GUI/yes.png")
    b0 = Button(
        feedback_content,
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=btn_clicked,
        relief="flat"
    )
    b0.place(x=119, y=154, width=81, height=30)

    img3 = PhotoImage(file="./GUI/no.png")
    b3 = Button(
        feedback_content,
        image=img3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: switch_buttons(b0, b3, b1, b2),
        relief="flat"
    )
    b3.place(x=292, y=154, width=81, height=30)

    feedback_content.create_text(
        233.0, 50.0,
        text=sys.argv[1],
        fill="#ffffff",
        font=("Poppins-Regular", int(17.0))
    )

    background_img = PhotoImage(file="./GUI/fb-bg.png")
    background = feedback_content.create_image(
        194.5, 63.0,
        image=background_img
    )

    def switch_buttons(button1, button2, button3, button4):
        button1.destroy()
        button2.destroy()
        img1 = PhotoImage(file="./GUI/paper.png")
        button3.image = img1
        button3.config(image=img1, command=paper_button)
        button3.place(x=119, y=154, width=81, height=30)
        img2 = PhotoImage(file="./GUI/plastic.png")
        button4.image = img2
        button4.config(image=img2, command=plastic_button)
        button4.place(x=292, y=154, width=81, height=30)

    img1 = PhotoImage(file="./GUI/paper.png")
    b1 = Button(
        feedback_content,
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=paper_button,
        relief="flat"
    )
    b1.image = img1

    img2 = PhotoImage(file="./GUI/plastic.png")
    b2 = Button(
        feedback_content,
        image=img2,
        borderwidth=0,
        highlightthickness=0,
        command=plastic_button,
        relief="flat"
    )
    b2.image = img2

    feedback_window.mainloop()





# END
window = Tk()

window.geometry("480x320")
window.configure(bg = "#292929")
canvas = Canvas(
    window,
    bg = "#292929",
    height = 320,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"./GUI/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = done_clicked,
    relief = "flat")

b0.place(
    x = 92, y = 254,
    width = 81,
    height = 30)

img1 = PhotoImage(file = f"./GUI/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_feedback,
    relief = "flat")

b1.place(
    x = 316, y = 254,
    width = 81,
    height = 30)

canvas.create_text(
    237.5, 194.0,
    text = "Detected class is:" + sys.argv[1] + " " + sys.argv[2],
    fill = "#ffffff",
    font = ("Poppins-Regular", int(17.0)))

background_img = PhotoImage(file = f"./GUI/background.png")
background = canvas.create_image(
    239.5, 90.5,
    image=background_img)

window.resizable(False, False)
window.mainloop()
