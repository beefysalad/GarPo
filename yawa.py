import tensorflow as tf

# Disable tensorflow compilation warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def analyse(image_path):
    # Read the image data
    with tf.gfile.FastGFile(image_path, 'rb') as f:
        image_data = f.read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile("./tf_files/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("./tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image data as input to the graph and get the first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        # Create a dictionary of class labels and their scores
        obj = {}
        for node_id in top_k:
            human_string = label
