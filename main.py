import os
from sqlite3 import ProgrammingError
import nltk # pip install nltk
#import syllables # pip install syllables
from nltk.tokenize import word_tokenize
#nltk.download()

import random
from nltk.tokenize.treebank import TreebankWordDetokenizer as tbdetok


text = word_tokenize("punching zombies at night\ncreepers give a big fright\nmine diamonds")
print(nltk.pos_tag(text))

# reading in + tagging the minecraft-related words
mineWords = []
with open("words.txt",'r', encoding="utf8") as a: # first, read txt file into a list
        mineWords = a.read().splitlines()

print(mineWords)
print(type(mineWords))
mineWordsTag = nltk.pos_tag(mineWords)
print(mineWordsTag)

# reading in the lyrics
lyricFile = "enemyShort.txt"
lyrics = []
with open(os.path.join("lyrics", lyricFile),'r', encoding="utf8") as a: # first, read txt file into a list
        lyrics = a.readlines()

print(lyrics)

# tagging the lyrics

lyricsTok = word_tokenize(lyrics)
lyricsTag = nltk.pos_tag(lyricsTok)

# replace words in the lyrics with words from mineWords with the same POS
funnyLyrics = ""


# takes in a tokenized (word, pos) pair from lyrics
# and full list of tokenized mineWords
def replaceWord(lyricWord, taggedMineWords):
    word = lyricWord[0]
    tag = lyricWord[1]

    matchMineWords = [] # array of mineWords that match POS

    for mWord, mTag in taggedMineWords: # search through mineWords
        if tag == mTag: # match found
            matchMineWords.append(mWord) # add to the matched words

    print(matchMineWords)

    if (len(matchMineWords) > 0): # there is at least one matching word
        # choose random word from list
        return random.choice(matchMineWords)
    else:
        return word # return og word

# for processing one line of lyrics
def processLine(line):
    lineTok = word_tokenize(line)
    lineTag = nltk.pos_tag(lineTok)
    
    for i in range(len(lyricsTok)):
        lineTup = lineTag[i]

    lyricsTok[i] = replaceWord(lineTup, mineWordsTag)



print(lyricsTok)

funnyLyrics = tbdetok().detokenize(lyricsTok)
print(funnyLyrics)

