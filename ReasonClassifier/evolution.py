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
while generation <= generations:
    while x>0.001:
        while y>0.001:
            delta1 = m.train(X, y, hidden_neurons=Hn, alpha=(alpha), epochs=100000, dropout=False, dropout_percent=0.2)
            with open("log.txt", 'a') as out:
                delta1 = str(delta1)+": "+str(Hn)+" "+str(alpha)
                out.write(delta1 + '\n')
            delta2 = m.train(X, y, hidden_neurons=Hn+x, alpha=(alpha+(y/10)), epochs=100000, dropout=False, dropout_percent=0.2)
            with open("log.txt", 'a') as out:
                delta1 = str(delta2)+": "+str((Hn+x))+" "+str((alpha+(y/10)))
                out.write(delta2 + '\n')
            delta3 = m.train(X, y, hidden_neurons=Hn-x, alpha=(alpha-(y/10)), epochs=100000, dropout=False, dropout_percent=0.2)
            with open("log.txt", 'a') as out:
                delta1 = str(delta3)+": "+str((Hn-x))+" "+str((alpha-(y/10)))
                out.write(delta3 + '\n')
            if delta1<delta:
                delta = delta1
                Hn = Hn
                alpha = alpha
            if delta2<delta:
                delta = delta2
                Hn = Hn + x
                alpha = (alpha+(y/10))
            if delta3<delta:
                delta = delta3
                Hn = Hn - x
                alpha = (alpha-(y/10))
            y = y/10
        x = x/10
    print("Generation is:")
    print(generaion)
    generaion = generation + 1

print(delta)
print(alpha)
print(Hn)
