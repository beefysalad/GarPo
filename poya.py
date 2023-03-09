import tensorflow.compat.v1 as tf

# Load the frozen GraphDef
with tf.gfile.GFile('./tf_files/retrained_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

# Replace the BatchNormWithGlobalNormalization operation with tf.nn.batch_normalization
for node in graph_def.node:
    if node.op == 'BatchNormWithGlobalNormalization':
        node.op = 'FusedBatchNorm'
        node.attr['epsilon'].f = 0.001
        node.attr['is_training'].b = False
    elif node.op == 'BatchNormWithGlobalNormalizationV2':
        node.op = 'FusedBatchNorm'
        node.attr['epsilon'].f = 0.001
        node.attr['is_training'].b = False

# Create a new GraphDef with the modified nodes
output_graph_def = tf.GraphDef()
output_graph_def.node.extend(graph_def.node)

# Save the new GraphDef
with tf.gfile.GFile('model_modified.pb', 'wb') as f:
    f.write(output_graph_def.SerializeToString())

# Convert the modified GraphDef to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_frozen_graph('model_modified.pb', input_arrays=['DecodeJpeg/contents'], output_arrays=['final_result'])
tflite_model = converter.convert()
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
