import cv2
import numpy as np
import tensorflow as tf

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="./model.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define the class names
class_names = ['paper', 'plastic']

# Open a connection to the webcam
cap = cv2.VideoCapture(1)

# Loop through frames from the webcam
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Resize the frame to match the model's input shape
    resized_frame = cv2.resize(frame, (300, 300))
    
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
    
    # Get the class name for the predicted class
    class_name = class_names[class_idx]
    
    # Display the class name and confidence rate on the frame
    text = f"{class_name} ({confidence:.2f})"
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Show the frame
    cv2.imshow('frame', frame)
    
    # Exit the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
