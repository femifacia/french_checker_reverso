#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import time
import sys
from requests_html import HTMLSession
#import dryscrape
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os


# Color code

RED = '\033[91m'
GREEN = '\033[92m'
WHITE = '\033[00m'

#Reverso URL

url_raw = "https://www.reverso.net/orthographe/correcteur-francais/#text="

# File descriptors for log files

fd_input = open('./input.txt', 'w')
fd_output = open('./output.txt', 'w')

def getTextFromPath(path : str) -> str:
    fd = open(sys.argv[1], 'r')
    text = fd.read()
#    print('before', text)
    text = text.replace('\n', '%250A')
    fd.close()
#    print('after')
    return (text)

# We get the text to check from the first arg

text = getTextFromPath(sys.argv[1])

#let's create our driver hehe

driver = Chrome(executable_path="./chromedriver")

#this function will check some part of text and will return the corrected version (and the old version too)

def CheckCorrectness(url_final : str, fd_input , fd_output , driver):
    original_string = ""
    updated_string = ""
#    print('my_url', url_final)
    driver.get(url_final)
    driver.refresh()
    time.sleep(5)
    #         driver.set_page_load_timeout(120)
    btn = driver.find_elements(by=By.CLASS_NAME, value='speller-actions-input_button')
#    print(btn)
    #input()
    btn[0].click()
    #input()

    time.sleep(5)
    #copy_button = driver.find_elements(by=By.CLASS_NAME, value='speller-box__copy-button')
    copy_button = driver.find_elements(by=By.CLASS_NAME, value='speller-header__button')

    soup = BeautifulSoup(driver.page_source, 'lxml')
    div = soup.find('div', {'id':'textResult'})
    ngx_spellers = div.find_all('ngx-speller-corrected-phrase')
    for ngx_speller in ngx_spellers:
        span = ngx_speller.find('span', {'class':'corrected-phrase'})
        old_word = span['data-originaltext']
        new_word = ngx_speller.text
        if (new_word != old_word):
            original_string += RED
            updated_string += GREEN
        original_string += old_word
        updated_string += new_word
        if (new_word != old_word):
            original_string += WHITE
            updated_string += WHITE
    return original_string, updated_string
#    print(div.text)

# we set the limit of chars to push for each push

limit = 320
original_text = ''
updated_text = ''
size = len(text)

# a loop to check all the text even if it exceed the limit

while (size > 0):
    if size > limit:
        to_add = text[:limit + 1]
        text = text[limit:]
    else:
        to_add = text
        text = ""
    url = url_raw + to_add
    size = len(text)
    old,  new = CheckCorrectness(url,fd_input,fd_output,driver)
    original_text += old
    updated_text += new

# we print the old and corrected text

print('----------Original version----------')
print(original_text)
print('')
print('----------Corrected version----------')
print(updated_text)

original_text = original_text.replace(RED, '[')
original_text = original_text.replace(WHITE, ']')

updated_text = updated_text.replace(GREEN, '[')
updated_text = updated_text.replace(WHITE, ']')

# we save texts into two files, input.txt fot the original text and output.txt for corrected text

fd_input.write(original_text)
fd_output.write(updated_text)

driver.close()
fd_input.close()
fd_output.close()

# By DIAVOLLLOOOOO or Femi