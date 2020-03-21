import tensorflow as tf
import tensorflow.keras as keras

mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

#from tensorflow.keras.utils import to_categorical
#training_labels = to_categorical(training_labels, 10)
#test_labels = to_categorical(test_labels, 10)

#import matplotlib.pyplot as plt
#plt.imshow(training_images[0])
#plt.show()



train_images = train_images / 255.0
test_images = test_images / 255.0

train_images = train_images.reshape(train_images.shape[0],train_images.shape[1],train_images.shape[2],1)
test_images = test_images.reshape(test_images.shape[0],test_images.shape[1],test_images.shape[2],1)

model = keras.Sequential([
            keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
            keras.layers.MaxPooling2D(pool_size=(2,2)),
#            keras.layers.Conv2D(32, (3,3), activation='relu'),
#            keras.layers.MaxPooling2D(2,2),
            keras.layers.Flatten(),
            keras.layers.Dropout(0.4),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dropout(0.4),
            keras.layers.Dense(10, activation=tf.nn.softmax)
            ])


model = keras.Sequential()
model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28,28,1)))
model.add(keras.layers.Activation("relu"))
#model.add(keras.layers.BatchNormalization())

model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
#model.add(keras.layers.BatchNormalization(axis=-1))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
# model.add(keras.layers.Dropout(0.25))
# # second CONV => RELU => CONV => RELU => POOL layer set
#model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(keras.layers.BatchNormalization(axis=-1))
#model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(keras.layers.BatchNormalization(axis=-1))
#model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
# model.add(keras.layers.Dropout(0.25))
# # first (and only) set of FC => RELU layers

model.add(keras.layers.Flatten())
model.add(keras.layers.Dropout(0.25))
model.add(keras.layers.Dense(128, activation=tf.nn.relu))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dropout(0.25))
model.add(keras.layers.Dense(10, activation=tf.nn.softmax))


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
              )


model.fit(train_images, train_labels, epochs=6)

model.evaluate(test_images, test_labels)

predictions = model.predict(test_images)
i=0
n=0
for p in predictions:
    print(i, end='\t')
    print(p.argmax(), end='\t')
    print(test_labels[i])
    if p.argmax()==test_labels[i]:
        n += 1
    i += 1

 