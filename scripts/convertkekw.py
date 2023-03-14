import tensorflow as tf

# Load the SavedModel format model
model = tf.compat.v1.saved_model.load('./tf_files/retrained_graph.pb')

# Convert the TensorFlow 2.x model to a TensorFlow Lite model
converter = tf.lite.TFLiteConverter.from_saved_model('./tf_files/retrained_graph.pb',tags=['serve'])
tflite_model = converter.convert()

# Save the converted TensorFlow Lite model to a file
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
