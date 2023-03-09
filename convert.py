import tensorflow.compat.v1 as tf

# Define the input and output paths for the .pb file and the .tflite file
pb_path = './tf_files/retrained_graph.pb'
tflite_path = './model.tflite'

# Load the .pb file as a TensorFlow graph
with tf.io.gfile.GFile(pb_path, 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

# Create a new TensorFlow session and graph
with tf.compat.v1.Session() as sess:
    # Import the graph definition into the new TensorFlow session
    tf.import_graph_def(graph_def, name='')
    
    # Get the input and output tensors
    input_tensor = sess.graph.get_tensor_by_name('DecodeJpeg/contents:0')
    output_tensor = sess.graph.get_tensor_by_name('final_result:0')

    # Convert the TensorFlow graph to a TensorFlow Lite model
    converter = tf.lite.TFLiteConverter.from_session(sess, [input_tensor], [output_tensor])
    converter.allow_custom_ops = True
    converter.experimental_new_converter = True
    converter.experimental_new_quantizer = True
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    tflite_model = converter.convert()

# Save the TensorFlow Lite model to disk
with tf.io.gfile.GFile(tflite_path, 'wb') as f:
    f.write(tflite_model)
