#!/usr/bin/python3.6

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import get_games
import chess_feeder
import numpy
import json
import os

numpy.random.seed(3);

token = str(open("token","r").read()).replace("\n","");
user = "georgerapeanu";

print("getting games");

inputs,outputs = chess_feeder.feed_games(get_games.get_games(user,token));
inputs = numpy.array(inputs);
outputs = numpy.array(outputs);


print("model starts here");

model = Sequential();

model.add(Dense(8 * 8 * 12,input_dim = 8 * 8 * 12,activation = 'relu'));
model.add(Dense(5000,activation = 'relu'));
model.add(Dense(5000,activation = 'relu'));
model.add(Dense(5000,activation = 'relu'));
model.add(Dense(8 * 8 * 8 * 8,activation = 'sigmoid'));

model.compile(loss = 'categorical_crossentropy',optimizer = 'adam',metrics = ['accuracy'])

model.fit(inputs,outputs, epochs = 10,batch_size = 20)
 
_,acc = model.evaluate(inputs,outputs);

print("Accuracy: %.2f" % (acc * 100));
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")
print("Saved model to disk")
