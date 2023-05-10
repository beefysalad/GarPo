import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import RPi.GPIO as GPIO
import subprocess
import time
import requests
from datetime import datetime

# Load the TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="./FINALE_WEIGHTS/inception_final.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define the class names
class_names = ['nothing', 'paper', 'plastic']
points = 0
class_name = " "
# Set up the GPIO pins for the IR sensor
IR_SENSOR_PIN = 21
#INDUCTIVE_SENSOR_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
#GPIO.setup(INDUCTIVE_SENSOR_PIN, GPIO.IN)

metal_counter = 0
paper_counter = 0
plastic_counter = 0
paper_level = ''
metal_level = ''
plastic_level =''
current_date = datetime.today().strftime('%Y-%m-%d')

with open('text_files/points.txt', 'w') as f:
    f.write(str(points))
with open('text_files/class.txt', 'w') as f:
    f.write(class_name)
with open('text_files/date_stored.txt', 'w') as f:
    f.write(current_date)


def update_counter():
    with open('text_files/counter_metal.txt', 'w') as f:
        f.write(str(metal_counter))
    with open('text_files/counter_plastic.txt', 'w') as f:
        f.write(str(plastic_counter))
    with open('text_files/counter_paper.txt', 'w') as f:
        f.write(str(paper_counter))
# Continuously capture images from the webcam and perform inference when IR sensor is triggered

subprocess.Popen(['python','./GUI/window.py',class_name,str(points)])
# Load the stored date from a file
while True:
    # Check if IR sensor is triggered
    if not GPIO.input(IR_SENSOR_PIN) == GPIO.HIGH:
        check_current_date = datetime.today().strftime('%Y-%m-%d')
        with open('text_files/points.txt', 'r') as f:
            points = int(f.read().strip())
        with open('text_files/class.txt', 'r') as f:
            class_name = f.read()
        with open('text_files/date_stored.txt','r') as f:
            current_date = f.read()
        with open('plastic_bin_levels.txt', 'r') as f:
            plastic_level = f.read().strip()
        with open('paper_bin_levels.txt', 'r') as f:
            paper_level = f.read().strip()
        with open('metal_bin_levels.txt', 'r') as f:
            metal_level = f.read().strip()
        #check this code remove if it creates bugs

        if check_current_date != current_date:
            print("nisud",metal_counter,paper_counter,plastic_counter)
            metal_counter=0
            paper_counter=0
            plastic_counter=0
            with open('text_files/date_stored.txt', 'w') as f:
                current_date = check_current_date
                f.write(current_date)
            
        time.sleep(2)            
        #if not GPIO.input(INDUCTIVE_SENSOR_PIN) == GPIO.HIGH:
            #print("METAL DETECTED")
           # if metal_level != 'full':
                #metal_counter+=1
                #update_counter()
                #points+=3
                #with open('text_files/points.txt', 'w') as f:
                    #f.write(str(points))
                #with open('text_files/class.txt', 'w') as f:
                    #f.write('metal')
                #subprocess.call(["python","servo_rotation.py","metal"])
                #time.sleep(0.5)
                #continue
            #elif metal_level == 'full':
                #class_name = 'METAL BIN FULL'
                #DIRI NAG END ANG AKONG NEW CODE#
            #metal_counter+=1
            #update_counter()
            #points+=3
            #with open('text_files/points.txt', 'w') as f:
                #f.write(str(points))
            #with open ('text_files/class.txt', 'w') as f:
                #f.write('metal')
            #subprocess.call(["python","servo_rotation.py","metal"])
            #time.sleep(0.5)
            #continue
        # Capture an image using raspistill

        ## note: remove -n to show the image capturing
        subprocess.call(['raspistill', '-o', 'image.jpg','-t','1000'])

        # Load the captured image and resize it to the required input size of the model
        frame = cv2.imread('image.jpg')
        frame=cv2.resize(frame,(480,320))
        resized_frame = cv2.resize(frame, (299, 299))

        # Preprocess the frame
        preprocessed_frame = np.array(resized_frame, dtype=np.float32) / 255.0

        # Set the input tensor to the preprocessed frame
        interpreter.set_tensor(input_details[0]['index'], np.expand_dims(preprocessed_frame, axis=0))

        # Run the inference
        interpreter.invoke()

        # Get the output tensor
        prediction = interpreter.get_tensor(output_details[0]['index'])

        # Get the class label with the highest probability
        class_idx = np.argmax(prediction)

        # Get the confidence rate for the predicted class
        confidence = prediction[0][class_idx]
        # If the predicted class is not "nothing" and the confidence is above 80%
        if confidence >= 0.70:
            # Get the class name for the predicted class
            class_name = class_names[class_idx]

            # Display the class name and confidence rate on the frame
            text = f"{class_name} ({confidence:.2f})"
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                
            # Check if the predicted class is "plastic" or "paper"
            if class_name == 'plastic' and plastic_level != 'full':
                print("NISUD PLASTIC", confidence)
                plastic_counter+=1
                update_counter()
                points += 2
                #subprocess.call(["python","servo_rotation.py","plastic"])
            elif class_name == 'plastic' and plastic_level == 'full':
                class_name = 'PLASTIC BIN FULL'
            elif class_name == 'paper' and paper_level != 'full':
                print("NISUD PAPER", confidence)
                paper_counter+=1
                update_counter()
                points += 1
                #subprocess.call(["python","servo_rotation.py","paper"])
            elif class_name =='paper' and paper_level == 'full':
                class_name = 'PAPER BIN FULL'
            with open('text_files/points.txt', 'w') as f:
                f.write(str(points))
            with open ('text_files/class.txt', 'w') as f:
                f.write(class_name)

        else:
            print(class_names[class_idx], confidence)
        



        

GPIO.cleanup()

#cv2.destroyAllWindows()
