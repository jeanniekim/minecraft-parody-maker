import os
from sqlite3 import ProgrammingError
from tokenize import String
from xml.etree.ElementTree import TreeBuilder
import nltk # pip install nltk
#import syllables # pip install syllables
from nltk.tokenize import word_tokenize
#nltk.download()

import random
from nltk.tokenize.treebank import TreebankWordDetokenizer as tbdetok

import csv


### *** PART OF SPEECH MATCHING ***

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
lyricFile = "creepShort.txt"
lyrics = []
with open(os.path.join("lyrics", lyricFile),'r', encoding="utf8") as a: # first, read txt file into a list
        lyrics = a.readlines()

print(lyrics)

# tagging the lyrics

#lyricsTok = word_tokenize(lyrics)
#lyricsTag = nltk.pos_tag(lyricsTok)

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
        # capital matching
        if word[0].isupper(): # capitalized
            finalWord = random.choice(matchMineWords).capitalize()
        #elif word.isupper(): # all caps
        #    finalWord = random.choice(matchMineWords).upper()
        else:
            finalWord = random.choice(matchMineWords)
        return finalWord
    else:
        return word # return og word

# for processing one line of lyrics
def processLine(line):
    lineTok = word_tokenize(line)
    lineTag = nltk.pos_tag(lineTok)
    
    for i in range(len(lineTok)):
        lineTup = lineTag[i]
        lineTok[i] = replaceWord(lineTup, mineWordsTag)

    finalLine = tbdetok().detokenize(lineTok)
    return finalLine


# DO THE THINGY.

funnyLyrics = []

for line in lyrics:
    funnyLyrics.append(processLine(line))

funnyLyrics = "\n".join(funnyLyrics)
print(funnyLyrics)

funnyFile = lyricFile[:-4] + "Fun.txt"
with open(os.path.join("funnyLyrics", funnyFile),'w', encoding="utf8") as b: # first, read txt file into a list
    b.write(funnyLyrics)

### *** SYLLABLES ***

# http://www.onebloke.com/2011/06/counting-syllables-accurately-in-python-on-google-app-engine/

#pip install requests==2.19.1 twilio==6.16.0 flask==1.0.2
import requests
import pyrhyme # pip install pyrhyme

rhymebrain_url = 'http://rhymebrain.com/talk'

# read in csv file containing contraction syllables
contractions = dict()
with open("contractions.csv", 'r') as c:
    csvreader = csv.reader(c)
    for row in csvreader:
        contractions.update({row[0]: row[1]})

# get the number of syllables of any word (or string of words) using rhymebrain and csv
def getSyllables(word): 
    if '\'' in word: # word is a contraction
        capWord = word.capitalize() # csv uses capitialized words
        if capWord in contractions: # if there's a match
            return contractions.get(capWord) # return the syllables

    params = { 'function': 'getWordInfo', 'word': word }
    rhymebrain_response = requests.get(rhymebrain_url, params).json() 
    # rhymebrain_response is a dictionary with word information

    syllables = rhymebrain_response.get('syllables')

    return syllables
         

print(getSyllables("I don't belong here"))
