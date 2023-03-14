import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import cv2
import sys
import os

# Disable TensorFlow compilation warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def analyse(image_path):
    # Read the image data
    with tf.io.gfile.GFile(image_path, 'rb') as f:
        image_data = f.read()

    # Load the label file and strip off carriage returns
    label_lines = [line.rstrip() for line in tf.io.gfile.GFile("./tf_files/retrained_labels.txt")]

    # Load the TensorFlow model
    with tf.io.gfile.GFile("../tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image data as input to the graph and get the first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Filter out detections with a confidence level below 80%
        filtered_obj = {}
        for i in range(len(predictions[0])):
            score = predictions[0][i]
            if score >= 0.8:
                human_string = label_lines[i]
                filtered_obj[human_string] = float(score)

        return filtered_obj


result = analyse('./training_dataset/paper2.jpg')
print(result)