from tkinter import *
from tkinter import ttk
import requests
import os
import sys
import pyautogui
import tkinter as tk
import sys

filename = "./image.jpg"
filepath = os.path.join(os.getcwd(), filename)
qr_data = ""

metal_counter = 0
paper_counter = 0
plastic_counter = 0

def update_points():
    with open('points.txt','r') as f:
        points = f.read()
        canvas.itemconfig(label_points,text=points)
        
    with open('class.txt', 'r') as f:
        class_n = f.read()
        canvas.itemconfig(label_class,text=class_n)
    points = canvas.itemcget(label_points, 'text')
    
    window.after(100,update_points)
                
def btn_clicked():
    window.destroy()

def on_press2(event):
    global qr_data 
    url = 'http://localhost:8080/qr-data'
    #with open('points.txt','w') as f:
        #f.write(str(0))
    if event.name == 'enter':
        print("QR CODE SCANNED yawa:",qr_data)
        payload = {'data': qr_data,'points':'10'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url,json=payload, headers=headers)
        with open('points.txt', 'w') as f:
            f.write(str(0))
        if response.ok:
            print("GOOD")
            
        else:
            print("not good",response.status_code)
        qr_data = ""
    elif len(event.name) == 1 and event.name.isalnum():
       qr_data += event.name.upper() if keyboard.is_pressed('shift') else event.name.lower()
def reset_points ():
    with open('points.txt', 'w') as f:
        f.write(str(0))
        
    with open('class.txt', 'w') as f:
        f.write(" ")
        
def on_press():
    url = 'http://localhost:8080/qr-data'
    #with open('points.txt', 'w') as f:
        #f.write(str(0))
    try:
        print("NISUD 2")
        qr_data=pyautogui.password("Scan your QR CODE")
    except pyautogui.FailSafeException:
        print("NISUD")
        qr_data=None
    #qr_data=pyautogui.password("Scan your QR Code")
    
    if qr_data is None:
        b0.config(state='active')
        return
    print("QR CODE SCANNED:",qr_data)
    points = canvas.itemcget(label_points, 'text')
    print(points)
    payload = {'data':qr_data,'points':points}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url,json=payload, headers=headers)
        response.raise_for_status()
        if(response.ok):
            b0.config(state='active')
            reset_points()
    except requests.exceptions.RequestException as e:
        print("Request exception:", str(e))
        b0.config(state='active')
        
    #response = requests.post(url,json=payload,headers=headers)
    
    #if(response.ok):
        #window.destroy()
        #print("GOOD")
        #b0.config(state='active')
        #reset_points()
    #else:
        #print("NOT GOOD")
        #b0.config(state='active')
    
    
def update_statistics():
    try:
        with open('counter_metal.txt', 'r') as f:
            metal_counter = int(f.read().strip())
    except FileNotFoundError:
        # Handle file not found error
        metal_counter = 0
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while reading 'counter_metal.txt': {str(e)}")
        return

    try:
        with open('counter_plastic.txt', 'r') as f:
            plastic_counter = int(f.read().strip())
    except FileNotFoundError:
        # Handle file not found error
        plastic_counter = 0
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while reading 'counter_plastic.txt': {str(e)}")
        return

    try:
        with open('counter_paper.txt', 'r') as f:
            paper_counter = int(f.read().strip())
    except FileNotFoundError:
        # Handle file not found error
        paper_counter = 0
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred while reading 'counter_paper.txt': {str(e)}")
        return

    stats_url = 'http://localhost:8080/statistics'
    payload = {'Paper': paper_counter, 'Plastic': plastic_counter, 'Metal': metal_counter}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(stats_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        print("Statistics updated successfully")
    except requests.exceptions.RequestException as e:
        # Handle request exception
        print(f"An error occurred while updating statistics: {str(e)}")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred during the request: {str(e)}")
def done_clicked():
    update_statistics()
    b0.config(state="disabled")
    on_press()
    
    #keyboard.on_press(on_press)
    #window.destroy()


    

def btn_feedback():
    with open ('class.txt', 'r') as f:
        class_n = f.read().strip()
    if class_n:
        
        feedback_window = Toplevel()
        feedback_window.title("Feedback")
        feedback_window.geometry("480x320")
        def plastic_button():
            folder_name = 'plastic'
            url = 'http://localhost:8080/upload?folder=' + folder_name
            files = {'image': open(filepath, 'rb')}
            feedback_window.destroy()
            response = requests.post(url, files=files)
            print(response)
            
        def paper_button():
            print("PAPER")
            folder_name = 'paper'
            url = 'http://localhost:8080/upload?folder=' + folder_name
            files = {'image': open(filepath, 'rb')}
            feedback_window.destroy()
            response = requests.post(url, files=files)
            print(response)
            
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
            text=canvas.itemcget(label_class,'text'),
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
    else:
        print("FEEDBACK NOT AVAIL")
        #b0.config(state='disabled')

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
    x = 121, y = 230,
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
    x = 292, y = 230,
    width = 81,
    height = 30)

label_points = canvas.create_text(
    323.5, 198.0,
    text = "0",
    fill = "#ffffff",
    font = ("Poppins-Regular", int(17.0)))

label_class = canvas.create_text(
    250.0, 171.0,
    text = " ",
    fill = "#ffffff",
    font = ("Poppins-Regular", int(17.0)))

background_img = PhotoImage(file = f"./GUI/background.png")
background = canvas.create_image(
    245.5, 113.0,
    image=background_img)

window.resizable(False, False)
update_points()
window.mainloop()
