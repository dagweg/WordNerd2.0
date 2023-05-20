import random
import csv
from functools import wraps
from flask import url_for, redirect, session
from cs50 import SQL

db = SQL('sqlite:///wordnerd.db')

difficulty = ['Easy', 'Medium', 'Hard', 'Insane']

# dictionary grouped by difficulty
dictionary = {
    'easy'    : {},
    'medium'  : {},
    'hard'    : {},
    'insane'  : {}
}

compliments = [ 'Superb!', 'Phenomenal!','Fantastic!', 'Excellent!', 'Well-Informed!', 'Megamind!', 'Brilliant!','You-on-Fire!', 'Genius!', 'Epic!', 'Bravo!' ]

def encrPw(password):
    pwd = list(password)
    hash = ''
    for c in pwd:
       hash += chr(ord(c)+10)
    return hash

def getPw(hash):
    pwd = ''
    for c in hash:
        pwd += chr(ord(c) - 10)
    return pwd

def get_rand_word(diff):
    k = random.choice(list(dictionary[diff].keys()))
    return str(k)

def scramble(word):
    word = list(word)
    scr = word[:]

    for i in range(0, len(scr)-1):
        rand = random.randint(i+1, len(scr)-1)
        temp = scr[i]
        scr[i] = scr[rand]
        scr[rand] = temp
    scrambled=''
    for strs in scr:
        for ch in strs:
            scrambled+=ch
    return str(scrambled)

def randCompl():
    return compliments[random.randint(0,len(compliments)-1)]

def parseCSV():
    ## CSV Parsing
    with open('dictionary.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter='\n')
        for line in csv_reader:
            for string in line:
                try:
                    word = string.split('=')[0].strip()
                    defn = string.split('=')[1].strip()
                except IndexError:
                    continue
                
                ## storing csv data into the dictionary based on difficulty (word-length)
                if (4 <= len(word) <= 5):
                    dictionary['easy'][word] = defn     # Easy
                elif (6 <= len(word) <= 7):  
                    dictionary['medium'][word] = defn   # Medium
                elif (8 <= len(word) <= 9):
                    dictionary['hard'][word] = defn     # Hard
                else:
                    dictionary['insane'][word] = defn   # Insane
        
        ## Removing weird words from the dict (SOME DEVIANTS GOTTA GO!! :))
        invalidTokens = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']


        for k in dictionary['insane'].copy():
            for ch in k:
                if ch in invalidTokens:
                    del dictionary['insane'][str(k)]
                    break
        for k in dictionary['easy'].copy():
            for ch in k:
                if ch in invalidTokens:
                    del dictionary['easy'][str(k)]
                    break
        for k in dictionary['medium'].copy():
            for ch in k:
                if ch in invalidTokens:
                    del dictionary['medium'][str(k)]
                    break
        for k in dictionary['hard'].copy():
            for ch in k:
                if ch in invalidTokens:
                    del dictionary['hard'][str(k)]
                    break

def getHint(diff, word):
    return dictionary[diff][word]

def login_required(f):
    @wraps(f)

    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
