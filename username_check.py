#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 21:49:29 2019
"""

import json
import requests
from time import sleep

# Settings
USERNAME_LENGTH = 4 #length of the word to check for reddit usernames. lower = cooler.
REQUEST_DELAY = 1 #seconds to delay after each reddit request

# Verify using the reddit API if the username exists or not 
# Code based on https://github.com/cutted/reddit-username-checker/blob/master/reddit.py

def check(name):
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.3"
    headers = {"user-agent": ua}
    params = {"user": name}
    
    request = requests.get('https://www.reddit.com/api/username_available.json', params=params, headers=headers)
    text = request.text
    if text == "true": # Username exists condition
        return [name, True]

    else: #Username does not exist
        return [name, False]


with open('process_dict.json', 'r') as dfile:
    letdic = json.load(dfile)

words_with_four_letters = []

for alphastr in letdic:
    if len(alphastr) != USERNAME_LENGTH:
        continue
    words_with_four_letters += letdic[alphastr]

# Eliminate the uniques
unique_words = set()

for word in words_with_four_letters:
    unique_words.add(word)

unique_words = sorted(list(unique_words))

print('{} total words with {} letters'.format(len(unique_words), USERNAME_LENGTH))
print(unique_words[0:10])

# Loop through all the word 4 letter usernames to find ones which are not taken

available = [] # QUERY THIS ARRAY TO FIND THE AVAILABLE USERNAMES
unknown_error = []
taken = []
count = 0
for word in unique_words:
    count += 1
    if count%100==0:
        print('{} out of {}'.format(count, len(unique_words)))
    try:
        result = check(word)
        if result[1] == True:
            available += [result[0]]
            
        elif result[1] == False:
            taken += [result[0]]
            
        else:
            unknown_error += [word]
    except:
        unknown_error += [word]
    
    sleep(REQUEST_DELAY)
    
print(available)