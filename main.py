from utils import *
from parserUtils import *
from sentencePlanUtils import *
import os

os.chdir("/Users/aleclock/Desktop/uni/TLN/mazzei/progettoTLN_Mazzei")

def main():
    sentences = loadSentences("./resources/sentences.txt")
    lex = loadLexicon("./resources/eng_ita_lex.csv")

    for s in sentences:
        print ("Sentence: " + s)

        # ---------------------------------------------
        # ----  Sentence to formula
        # ---------------------------------------------

        tree = parseSentence (s, "./resources/simple-sem.fcfg")
        
        #printTreeImage(tree)
        #tree.draw()

        formula = tree.label()['SEM'].simplify() # simplify() apply beta-reduction
        print ("FOL: " + str(formula))

        # ---------------------------------------------
        # ----  Formula to sentence plan
        # By starting from regular expressions, parts of the sentence (predicates) and their value (arguments) are identified.
        # The translation of the arguments is performed and the generated sentence plan is used as input for the NLG phase.
        # ---------------------------------------------
        
        planT = getSentencePlan(formula, tree, lex) # create translated sentence plan

        #savePlanToJSON(planT, sentences.index(s))
        #print (planT)

        print ("\n***\n")
main()