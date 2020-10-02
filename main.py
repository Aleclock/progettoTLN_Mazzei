from utils import *
from parserUtils import *
import os

os.chdir("/Users/aleclock/Desktop/uni/TLN/mazzei/progettoTLN_Mazzei")

def main():
    sentences = loadSentences("./resources/sentences.txt")  # Al momento prende le prime quattro frasi (TODO modificare)
    for s in sentences:
        print ("Sentence: " + s)

        # ---------------------------------------------
        # ----  Sentence to formula
        # ---------------------------------------------

        trees = parseSentence (s, "./resources/simple-sem.fcfg")
        formula = trees.label()['SEM'].simplify()
        print (formula)

        # ---------------------------------------------
        # ----  Formula to sentence plan
        # ---------------------------------------------

        #translation = getSentencePlan(s, formula)

        # ---------------------------------------------
        # ----  Sentence plan to traslated sentence
        # ---------------------------------------------
        print ("---")
main()