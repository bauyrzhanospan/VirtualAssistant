# use natural language toolkit
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

delta = 0.3
Hn = 20
alpha = 0.1
generations = 100
generation = 0
x = 1
y = 1

delta1 = m.train(X, y, hidden_neurons=Hn, alpha=(alpha), epochs=20000, dropout=False, dropout_percent=0.2)
with open("log.txt", 'a') as out:
    delta1 = str(delta1)+": "+str(Hn)+" "+str(alpha)
    out.write(delta1 + '\n')
    print(delta1)
