import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import sys
import os

# Disable TensorFlow compilation warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def analyse(image_path):
    # Read the image data
    with tf.io.gfile.GFile(image_path, 'rb') as f:
        image_data = f.read()

    # Load the label file and strip off carriage returns
    label_lines = [line.rstrip() for line in  tf.io.gfile.GFile("./tf_files/retrained_labels.txt")]

    # Load the TensorFlow model
    with tf.io.gfile.GFile("../tf_files/retrained_graph.pb", 'rb') as f:
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

        return obj

result = analyse('./training_dataset/random.jpg')
print(result)