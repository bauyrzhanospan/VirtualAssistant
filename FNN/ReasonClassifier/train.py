#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime

stemmer = LancasterStemmer()
import numpy as np
import time
from lib import mods as m

words_file = "./include/words.json"
with open(words_file) as word_file:
    words = json.load(word_file)
classes_file = "./include/classes.json"
with open(classes_file) as class_file:
    classes = json.load(class_file)
output_file = "./include/output.json"
with open(output_file) as out_file:
    output = json.load(out_file)
training_file = "./include/training.json"
with open(training_file) as train_file:
    training = json.load(train_file)

X = np.array(training)
y = np.array(output)

start_time = time.time()

m.train(X, y, hidden_neurons=14, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2)

elapsed_time = time.time() - start_time
print("processing time:", elapsed_time, "seconds")
