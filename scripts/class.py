import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import sys
import os
import numpy as np
import cv2

# Disable TensorFlow compilation warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def analyse(image_path):
    # Read the image data
    with tf.io.gfile.GFile(image_path, 'rb') as f:
        image_data = f.read()

    # Load the label file and strip off carriage returns
    label_lines = [line.rstrip() for line in  tf.io.gfile.GFile("./tf_files/retrained_labels.txt")]

    # Load the TensorFlow model
    with tf.io.gfile.GFile("./tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image data as input to the graph and get the first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        obj = {}
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            obj[human_string] = float(score)

        # Load the image using OpenCV
        img = cv2.imread(image_path)

        # Get the image dimensions
        height, width, channels = img.shape

        # Reshape the input image data to have a shape of (height, width, channels)
        image_data = np.frombuffer(image_data, dtype=np.uint8)
        img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        # Loop over the top predictions and draw bounding boxes
        for i, node_id in enumerate(top_k):
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            label = "{}: {:.2f}%".format(human_string, score * 100)

            # Get the bounding box coordinates
            ymin, xmin, ymax, xmax = sess.run('DecodeJpeg/contents:0', feed_dict={'final_result:0': image_np_expanded})
            ymin = int(ymin[0][i] * height)
            xmin = int(xmin[0][i] * width)
            ymax = int(ymax[0][i] * height)
            xmax = int(xmax[0][i] * width)

            # Draw the bounding box and label on the image
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show the image with the bounding box and label
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return obj


result = analyse('./training_dataset/5.jpg')
print(result)