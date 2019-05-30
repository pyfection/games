

from keras.models import Sequential
from keras.layers import Dense


def make_model():
    model = Sequential()
    model.add(Dense(5, activation='relu', input_shape=(9,)))
    model.add(Dense(2, activation='softmax'))
    return model


if __name__ == "__main__":
    model = make_model()
    model.summary()