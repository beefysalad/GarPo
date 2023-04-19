import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import cv2
import sys
import os
import subprocess
import RPi.GPIO as GPIO

# Load the label file and strip off carriage returns
label_lines = [line.rstrip() for line in tf.io.gfile.GFile("./FINALE_WEIGHTS/updated_graph.txt")]
points = 0

# Load the TensorFlow model
with tf.io.gfile.GFile("./FINALE_WEIGHTS/updated_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image data as input to the graph and get the first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    # Set up the GPIO pins for the IR sensor
    IR_SENSOR_PIN = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
    with open('points.txt', 'w') as f:
        f.write(str(points))
    # Continuously capture images from the webcam and perform inference when IR sensor is triggered
    while True:
        # Check if IR sensor is triggered
        if not GPIO.input(IR_SENSOR_PIN) == GPIO.HIGH:
            # Capture an image using raspistill
            with open('points.txt', 'r') as f:
                points = int(f.read().strip())
                
            subprocess.call(['libcamera-still', '-o', 'image.jpg','-t','2000'])

            # Load the captured image and resize it to the required input size of the model
            frame = cv2.imread('image.jpg')
            frame=cv2.resize(frame,(480,320))
            resized_image = cv2.resize(frame, (224, 224))

            # Convert the resized image to a byte string
            image_data = cv2.imencode('.jpg', resized_image)[1].tostring()

            # Get the predictions
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

            # Filter out detections with a confidence level below 80%
            filtered_obj = {}
            for i in range(len(predictions[0])):
                score = predictions[0][i]
                human_string = label_lines[i]
                filtered_obj[human_string] = float(score)

            # Draw bounding boxes on the frame for the filtered detections
            for label, score in filtered_obj.items():
                (w, h), _ = cv2.getTextSize(f"{label}: {score:.2f}", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                if score >= 0.80:
                    cv2.rectangle(frame, (0, 0), (w + 10, h + 10), (0, 0, 0), -1)
                    cv2.putText(frame, f"{label}: {score:.2f}", (5, h + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    if(label=='plastic'):
                        print("NISUD PLASTIC")
                        points += 2
                    elif(label=='paper'):
                        print("NISUD PAPER")
                        points += 1
                    with open('points.txt', 'w') as f:
                        f.write(str(points))
                    #subprocess.Popen(['pkill', '-f', 'window.py']).wait()
                    #subprocess.Popen(['python','./GUI/window.py',label,str(points)])
                    #window_process = subprocess.Popen(['python','./GUI/window.py','-q',str(queue)])
                    subprocess.Popen(['pkill', '-f', 'window.py']); subprocess.Popen(['python','./GUI/window.py',label,str(points)])

                else:
                    trash_text_size, _ = cv2.getTextSize("TRASH NOT IDENTIFIED", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    cv2.putText(frame, "TRASH NOT IDENTIFIED", (5, h + trash_text_size[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    

            # Display the resulting frame
            
            #cv2.imshow('Object Detection', frame)
            #print(points)
            # Save the image with the classified class and confidence score
            cv2.imwrite('test.jpg', frame)

        # Check for key press events to quit the program
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Close the OpenCV windows
    cv2.destroyAllWindows()

# Clean up the GPIO pins
GPIO.cleanup()
