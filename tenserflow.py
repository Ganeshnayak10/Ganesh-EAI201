import tensorflow as tf
import numpy as np

X = np.array([-4, -2, 0, 1, 2, 4, 6], dtype=float)
y = -2 * X + 5

model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=[1])])

model.compile(optimizer='sgd', loss='mse')
model.fit(X, y, epochs=200, verbose=0)
weights, bias = model.layers[0].get_weights()
m = weights[0][0]
c = bias[0]
print("Real equation     : y = -2x + 5")
print("Learned equation  : y = {:.2f}x + {:.2f}".format(m, c))
print("Slope             : {:.2f}".format(m))
print("Intercept         : {:.2f}".format(c))

