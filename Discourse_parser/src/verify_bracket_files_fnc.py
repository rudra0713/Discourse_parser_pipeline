import os, sys, shutil, pickle


bracket = pickle.load(open('../fnc_complete_1/fnc_article_brackets_1.p', 'rb'))
for key in bracket:
    print(key)
    print(bracket[key])
    break