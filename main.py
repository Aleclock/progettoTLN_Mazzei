from utils import *
from parserUtils import *
from sentencePlanUtils import *
import os

os.chdir("/Users/aleclock/Desktop/uni/TLN/mazzei/progettoTLN_Mazzei")

def main():
    sentences = loadSentences("./resources/sentences.txt")  # Al momento prende le prime quattro frasi (TODO modificare)
    lex = loadLexicon("./resources/eng_ita_lex.csv")

    for s in sentences[:]:
        print ("Sentence: " + s)

        # ---------------------------------------------
        # ----  Sentence to formula
        # ---------------------------------------------

        tree = parseSentence (s, "./resources/simple-sem.fcfg")
        print (tree)
        
        #saveTreeImage(tree)
        #tree.draw() # https://www.nltk.org/book/ch08.html
        """
        http://www.nltk.org/book/ch10.html
        The "reduction" of (36) to (37) is an extremely useful operation in simplifying semantic representations, and we shall use it a lot in the rest of this chapter. 
        The operation is often called β-reduction. In order for it to be semantically justified, we want it to hold that λx. α(β) has the same semantic values as α[β/x]. 
        This is indeed true, subject to a slight complication that we will come to shortly. In order to carry of β-reduction of expressions in NLTK, 
        we can call the simplify() method
        """
        formula = tree.label()['SEM'].simplify()

        # ---------------------------------------------
        # ----  Formula to sentence plan
        # ---------------------------------------------
        planT = getSentencePlan(formula, tree, lex) # Translated plan

        savePlanToJSON(planT, sentences.index(s))

        # ---------------------------------------------
        # ----  Sentence plan to traslated sentence
        # ---------------------------------------------

        print ("\n---\n")
main()