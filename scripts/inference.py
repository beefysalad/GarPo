import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import cv2
import sys
import os
import subprocess

def analyse():
    # Load the label file and strip off carriage returns
    label_lines = [line.rstrip() for line in tf.io.gfile.GFile("../updated_weights/today.txt")]

    # Load the TensorFlow model
    with tf.io.gfile.GFile("../updated_weights/today.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image data as input to the graph and get the first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        # Open the webcam
        cap = cv2.VideoCapture(1)

        # Continuously capture images from the webcam and perform inference when "v" is pressed
        while True:
            # Capture an image from the webcam
            ret, frame = cap.read()
            if not ret:
                print("Error: could not capture image")
                return

            # Display the frame
            cv2.imshow('Object Detection', frame)

            # Check for key press events
            key = cv2.waitKey(1) & 0xFF
            if key == ord('v'):
                # Resize the image to the required input size of the model
                resized_image = cv2.resize(frame, (224, 224))

                # Convert the resized image to a byte string
                image_data = cv2.imencode('.jpg', resized_image)[1].tostring()

                # Get the predictions
                predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

                # Filter out detections with a confidence level below 80%
                filtered_obj = {}
                for i in range(len(predictions[0])):
                    score = predictions[0][i]
                    if score >= 0.50:
                        human_string = label_lines[i]
                        filtered_obj[human_string] = float(score)

                # Draw bounding boxes on the frame for the filtered detections
                for label, score in filtered_obj.items():
                    (w, h), _ = cv2.getTextSize(f"{label}: {score:.2f}", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    cv2.rectangle(frame, (0, 0), (w + 10, h + 10), (0, 0, 0), -1)
                    cv2.putText(frame, f"{label}: {score:.2f}", (5, h + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    subprocess.Popen(['python','show_class.py',label])

                # Display the resulting frame
                cv2.imshow('Object Detection', frame)
        
                # Save the image with the classified class and confidence score
                cv2.imwrite('test.jpg', frame)

            # Quit the program when "q" is pressed
            elif key == ord('q'):
                break

        # Close the OpenCV windows
        cv2.destroyAllWindows()
        cap.release()

analyse()
