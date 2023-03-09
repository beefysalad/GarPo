import tensorflow.compat.v1 as tf
import cv2
import numpy as np

tf.disable_v2_behavior()

# Load the label file and strip off carriage returns
label_lines = [line.rstrip() for line in  tf.io.gfile.GFile("./tf_files/retrained_labels.txt")]

# Load the TensorFlow model
with tf.io.gfile.GFile("../tf_files/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Get the input and output tensors of the graph
    input_tensor = sess.graph.get_tensor_by_name('DecodeJpeg/contents:0')
    output_tensor = sess.graph.get_tensor_by_name('final_result:0')

    # Open the default web camera
    cap = cv2.VideoCapture(1)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Preprocess the frame to a serialized JPEG image
        _, jpeg = cv2.imencode('.jpg', frame)
        image_data = jpeg.tobytes()

        # Run the TensorFlow model on the serialized image to make predictions
        predictions = sess.run(output_tensor, {input_tensor: image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        obj = {}
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            obj[human_string] = float(score)

        # Draw the predictions on the frame
        for i, (label, score) in enumerate(obj.items()):
            if score < 0.5:  # Filter out low confidence predictions
                continue
            ymin, xmin, ymax, xmax = np.random.uniform(size=4)  # Placeholder values for bbox coordinates
            cv2.putText(frame, "{}: {:.2f}%".format(label, score*100), (10, 50 + i*20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(frame, (int(xmin*frame.shape[1]), int(ymin*frame.shape[0])),
                          (int(xmax*frame.shape[1]), int(ymax*frame.shape[0])), (0, 255, 0), 2)
        cv2.imshow('frame', frame)

        # Check if the 'q' key was pressed to exit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the resources
    cap.release()
    cv2.destroyAllWindows()
