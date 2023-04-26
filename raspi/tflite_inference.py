import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import RPi.GPIO as GPIO
import subprocess



# Load the TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path="./mobilenet_latest.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define the class names
class_names = ['nothing', 'paper', 'plastic']
points = 0
# Set up the GPIO pins for the IR sensor
IR_SENSOR_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
with open('points.txt', 'w') as f:
    f.write(str(points))
# Define initial points


# Continuously capture images from the webcam and perform inference when IR sensor is triggered
while True:
    # Check if IR sensor is triggered
    if not GPIO.input(IR_SENSOR_PIN) == GPIO.HIGH:
        # Capture an image using raspistill
        with open('points.txt', 'r') as f:
            points = int(f.read().strip())
			
        subprocess.call(['raspistill', '-o', 'image.jpg','-t','2000'])

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
            
            #subprocess.run(['pkill','-f','window.py'])
            subprocess.Popen(['python','./GUI/window.py',class_name,str(points)])
            
        else:
            print(class_names[class_idx], confidence)
        # Show the frame
        #cv2.imshow('frame', frame)

        # Exit the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
