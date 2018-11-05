import tensorflow as tf 
from tensorflow import keras

# Helper libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os

print(tf.__version__)

# Checkpoint
checkpoint_path = 'training/model.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, verbose=1)

# Read data
train = pd.read_csv('train_data.csv')
test = pd.read_csv('test_data.csv')

print('loading training and testing files...')
train_labels = (train.ix[:,-1].values).astype('uint8')
train_vector = (train.ix[:,:-1].values).astype('uint8')

test_vector = (test.ix[:,:-1].values).astype('uint8')
test_labels = (test.ix[:,-1].values).astype('uint8')

print('loading finished.')

train_vector = train_vector / 34.0
test_vector  = test_vector / 34.0

print(len(train_vector[:10000]))


# setup the layers
# model = keras.Sequential([
#     keras.layers.Dense(204),
#     keras.layers.Dense(120, activation=tf.nn.sigmoid),
#     keras.layers.Dense(110, activation=tf.nn.sigmoid),
#     keras.layers.Dense(110, activation=tf.nn.sigmoid),
#     keras.layers.Dense(100, activation=tf.nn.sigmoid),
#     keras.layers.Dense(34, activation=tf.nn.softmax)
# ])

group_size = 10000

# model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

counter = 1

# num_samples = []
# acc_samples = []

# while (counter < len(train_vector) // group_size):
#     model = keras.Sequential([
#         keras.layers.Dense(204),
#         keras.layers.Dense(120, activation=tf.nn.sigmoid),
#         keras.layers.Dense(110, activation=tf.nn.sigmoid),
#         keras.layers.Dense(110, activation=tf.nn.sigmoid),
#         keras.layers.Dense(100, activation=tf.nn.sigmoid),
#         keras.layers.Dense(34, activation=tf.nn.softmax)
#     ])

#     model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#     model.fit(train_vector[:counter*group_size], train_labels[:counter*group_size], epochs=10, callbacks = [cp_callback])
#     test_loss, test_acc = model.evaluate(test_vector, test_labels)
#     num_samples.append(counter*group_size)
#     acc_samples.append(test_acc)
#     print('Test accuracy (? training samples): ?', counter*group_size, test_acc)
#     counter += 1

model = keras.Sequential([
            keras.layers.Dense(204),
            keras.layers.Dense(120, activation=tf.nn.relu),
            keras.layers.Dense(110, activation=tf.nn.relu),
            keras.layers.Dense(110, activation=tf.nn.relu),
            keras.layers.Dense(100, activation=tf.nn.relu),
            keras.layers.Dense(14, activation=tf.nn.softmax)
        ])

model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_vector[:270000], train_labels[:270000], epochs=10, callbacks = [cp_callback])
test_loss, test_acc = model.evaluate(test_vector, test_labels)
# num_samples.append(len(train_vector))
# acc_samples.append(test_acc)
# print('Test accuracy (? training samples): ?', len(train_vector), test_acc)
print('Test accuracy: ', test_acc)
import h5py
import pypl

model.save('discard_model.h5')
# Show chart
# plt.plot(num_samples, acc_samples)
# plt.ylabel('Accuracy')
# plt.xlabel('Num of training samples')
# plt.show()
# Make predictions