import tensorflow as tf

# Define the input and output tensor names
input_tensor_name = 'input'
output_tensor_name = 'final_result'

# Load the optimized model graph from file
with tf.io.gfile.GFile('tf_files/graph_optimized.pb', 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_session(
    tf.compat.v1.Session(graph=tf.Graph()),
    [tf.compat.v1.placeholder(tf.float32, shape=[1, 224, 224, 3], name=input_tensor_name)],
    [tf.compat.v1.graph_util.make_list_of_constants(graph_def, [output_tensor_name])[0]],
    input_arrays=[input_tensor_name],
    output_arrays=[output_tensor_name])
tflite_model = converter.convert()

# Save the converted model to file
with open('optimized.tflite', 'wb') as f:
    f.write(tflite_model)
