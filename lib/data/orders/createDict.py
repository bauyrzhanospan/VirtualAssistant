import glob
import datetime
import os

memes = glob.glob('./*[!.py]')

for meme in memes:
    file = str(meme)
    newwords = []
    with open(file, "r") as word_file:
        for lines in word_file:
            words = str(lines).replace("\n", "").split(" ")
            words.append("the")
            phrase2 = ""
            for word in words:
                phrase2 = phrase2 + str(word) + " "
            words = words[1:] + words[:1]
            phrase = ""
            for word in words:
                phrase = phrase + str(word) + " "
            newwords.append(phrase)
            newwords.append(phrase2)
    print(newwords)
    with open(file, "a") as word_file:
        for phrase in newwords:
            word_file.write(str(phrase) + ", please\n")
            word_file.write("Please, " + str(phrase) + "\n")
            word_file.write("I need " + str(phrase) + "\n")
            word_file.write("I want " + str(phrase) + "\n")
            word_file.write("May I ask you to " + str(phrase) + "\n")
            word_file.write("You must " + str(phrase) + "\n")
            word_file.write("You have to " + str(phrase) + "\n")
