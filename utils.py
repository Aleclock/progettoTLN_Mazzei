from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
import os

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
    return sentences[:4]

def saveTreeImage(tree):
    cf = CanvasFrame()
    #t = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP pretty)))')
    tc = TreeWidget(cf.canvas(),tree)
    cf.add_widget(tc,30,30) # (10,10) offsets
    cf.print_to_file('output.ps')
    cf.destroy()