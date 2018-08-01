
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
ten = tf.constant(10)
thirty = tf.constant(32)
sess.run(ten + thirty)
sess.close()
