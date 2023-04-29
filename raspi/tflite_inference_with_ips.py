import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import RPi.GPIO as GPIO
import subprocess
import time


# Load the TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="./mobilenet_latest.tflite")
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
INDUCTIVE_SENSOR_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(INDUCTIVE_SENSOR_PIN, GPIO.IN)
with open('points.txt', 'w') as f:
    f.write(str(points))
with open('class.txt', 'w') as f:
    f.write(class_name)
# Define initial points



# Continuously capture images from the webcam and perform inference when IR sensor is triggered

subprocess.Popen(['python','./GUI/window.py',class_name,str(points)])
while True:
    # Check if IR sensor is triggered
    if not GPIO.input(IR_SENSOR_PIN) == GPIO.HIGH:
        with open('points.txt', 'r') as f:
            points = int(f.read().strip())
        with open('class.txt', 'r') as f:
            class_name = f.read()        
        time.sleep(2)            
        if not GPIO.input(INDUCTIVE_SENSOR_PIN) == GPIO.HIGH:
            print("METAL DETECTED")

            points+=3
            with open('points.txt', 'w') as f:
                f.write(str(points))
            with open ('class.txt', 'w') as f:
                f.write('metal')
            subprocess.call(['python', 'servo.py'])
            time.sleep(0.5)
            continue
        # Capture an image using raspistill

        ## note: remove -n to show the image capturing
        subprocess.call(['raspistill','-n', '-o', 'image.jpg','-t','1000'])

        # Load the captured image and resize it to the required input size of the model
        frame = cv2.imread('image.jpg')
        frame=cv2.resize(frame,(480,320))
        resized_frame = cv2.resize(frame, (224, 224))

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
        if confidence >= 0.8:
            # Get the class name for the predicted class
            class_name = class_names[class_idx]

            # Display the class name and confidence rate on the frame
            text = f"{class_name} ({confidence:.2f})"
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Check if the predicted class is "plastic" or "paper"
            if class_name == 'plastic':
                print("NISUD PLASTIC", confidence)
                points += 2
            elif class_name == 'paper':
                print("NISUD PAPER", confidence)
                points += 1
            with open('points.txt', 'w') as f:
                f.write(str(points))
            with open ('class.txt', 'w') as f:
                f.write(class_name)

        else:
            print(class_names[class_idx], confidence)


        

GPIO.cleanup()

#cv2.destroyAllWindows()
