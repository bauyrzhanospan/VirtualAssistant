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

training_data = m.make_dict()

print("%s sentences in training data" % len(training_data))

words = []
classes = []
documents = []
ignore_words = ['?', ',', '!']
# loop through each sentence in our training data
for pattern in training_data:
    # tokenize each word in the sentence
    w = nltk.word_tokenize(pattern['sentence'])
    # add to our words list
    words.extend(w)
    # add to documents in our corpus
    documents.append((w, pattern['class']))
    # add to our classes list
    if pattern['class'] not in classes:
        classes.append(pattern['class'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = list(set(words))

# remove duplicates
classes = list(set(classes))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique stemmed words", words)

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # create our bag of words array
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    training.append(bag)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    output.append(output_row)

print("# words", len(words))
print("# classes", len(classes))

words_file = "./include/words.json"
with open(words_file, 'w') as outfile:
    json.dump(words, outfile)
print("saved words to:", words_file)

classes_file = "./include/classes.json"
with open(classes_file, 'w') as outfile:
    json.dump(classes, outfile)
print("saved classes to:", classes_file)

training_file = "./include/training.json"
with open(training_file, 'w') as outfile:
    json.dump(training, outfile)
print("saved training to:", training_file)

output_file = "./include/output.json"
with open(output_file, 'w') as outfile:
    json.dump(output, outfile)
print("saved output to:", output_file)
