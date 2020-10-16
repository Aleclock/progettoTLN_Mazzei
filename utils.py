from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
import os
import pandas as pd
import csv
import json 

"""
Load document in path line by line
Input:  
    path: file path
Output: 
    sentences: list of sentences
"""
def loadSentences(path):
    sentences = []
    with open(path) as file:
        for line in file.readlines():
            sentences.append(line.replace("\n", "").lower())
    file.close()
    return sentences

"""
Load csv file and create a lexicon dictionary
Input:
    path: path file
Output:
    lexicon dictionary  {"eng_term", "ita_term"}
"""
def loadLexicon(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        return {rows[0]:rows[1] for rows in csv_reader}

"""
Save sentence plan as a JSON
Input:
    planT: translated sentence plan
    index: number of sentence (set file name)
"""
def savePlanToJSON(planT, index):
    with open("./output/sentence" + str(index) + ".json", 'w', encoding='utf-8') as f:
        json.dump(planT, f, ensure_ascii=False, indent=4)

"""
Print semantic tree 
Input:
    tree: semantic tree
"""
def printTreeImage(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(),tree)
    cf.add_widget(tc,30,30) # 30 offset
    cf.print_to_file('output.ps')
    cf.destroy()