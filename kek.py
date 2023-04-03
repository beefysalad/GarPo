import tensorflow as tf

# Load the optimized GraphDef
graph_def_file = "./tf_files/optimized_graph.pb"
with tf.io.gfile.GFile(graph_def_file, "rb") as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())

# Define input and output tensors
input_tensor = "DecodeJpeg/contents:0"
output_tensor = "final_result:0"

# Create converter object
converter = tf.compat.v1.lite.TocoConverter.from_frozen_graph(
    graph_def_file, input_tensors=[input_tensor], output_tensors=[output_tensor])

# Set TFLite model configurations
converter.inference_type = tf.compat.v1.lite.constants.QUANTIZED_UINT8
converter.quantized_input_stats = {input_tensor: (0., 1.)}  # (mean, std_dev)
converter.default_ranges_stats = (-128, 127)
converter.allow_custom_ops = True

# Convert the model to TFLite
tflite_model = converter.convert()

# Save the TFLite model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
