import tensorflow as tf
import numpy as np

dataPath = "data/snpdata.csv"

rawData = tf.contrib.data.make_csv_data_set(dataPath, batch_size=32)
data = [np.array(rawData)]
