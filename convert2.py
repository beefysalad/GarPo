import tensorflow as tf

# Load the SavedModel and convert it to a TFLite model
saved_model_path = './weights'
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
converter.experimental_new_converter = True
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,
    tf.lite.OpsSet.SELECT_TF
]
converter.ops_to_select = ['DecodeJpeg']

# Define the mean, variance, offset, and scale parameters
mean = 0.0
variance = 1.0
offset = 0.0
scale = 1.0

# Replace BatchNormWithGlobalNormalization with tf.nn.batch_normalization
def representative_dataset_gen():
    for image in image_data:
        yield [np.array(image, dtype=np.float32, ndmin=2)]
converter.representative_dataset = representative_dataset_gen
converter.representative_dataset = tf.function(representative_dataset_gen)
input_shape = [1,224,224,3]
image = tf.zeros(input_shape, dtype=tf.float32)
concrete_func = converter._get_concrete_function(inputs=[image])
converter.convert()

# Save the TFLite model to a file
tflite_model = converter.convert()
with open('models.tflite', 'wb') as f:
    f.write(tflite_model)
