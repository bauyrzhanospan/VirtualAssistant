import glob
import datetime
import os

memes = glob.glob('./[!create]*')

Health = ["need ", "prepare ", "going to ", "feel ", "will ", "have ", "must ", "want "]
Work = ["need ", "prepare ", "going to ", "will ", "feel ", "have ", "must ", "work ", "construct ", "design ",
        "write "]
Entertainment = ["want ", "going to ", "will ", "play ", "game "]
Food = ["prepare ", "going to ", "drink ", "will ", "have ", "eat ", "want "]
Security = ["need ", "secure ", "safe ", "have to "]
Energy = ["need ", "secure ", "safe ", "recycle ", "accumulate ", "have to "]

verbs = {'Health': Health, 'Work': Work, 'Entertainment': Entertainment, 'Energy': Energy, 'Food': Food,
         'Security': Security}
name = ["I ", "you ", "we ", "he ", "she ", "they "]
for meme in memes:
    file = str(meme)
    newwords = []
    with open(file, "r") as word_file:
        for lines in word_file:
            words = str(lines).replace("\n", "").split(" ")
            phrase2 = ""
            phrase = ""
            phrase1 = ""
            for word in words:
                phrase2 = phrase2 + str(word) + " "
            for v in verbs[str(meme[2:])]:
                for n in name:
                    phrase1 = str(n) + str(v) + phrase2 + "\n"
                    phrase = str(n) + phrase2 + "\n"
                    newwords.append(phrase1)
                    newwords.append(phrase)
    with open(file, "a") as word_file:
        for phrase in newwords:
            word_file.write(str(phrase))

# with open(file, "a") as word_file:
#        for phrase in newwords:
#            word_file.write(str(phrase) + ", please\n")
#            word_file.write("Please, " + str(phrase) + "\n")
