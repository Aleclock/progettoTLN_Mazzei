import nltk
from nltk import load_parser
import requests

"""
Apply NLTK parsing
Input:
    sentence: sentence to parse
    gramamr: CF grammar
        contains a small set of rules for parsing and translating simple examples of the kind that we have been looking at.
"""
def parseSentence(sentence, grammar):
    parser = load_parser(grammar, trace=0)
    trees = list(parser.parse(sentence.split()))
    
    # Analyzing FoL formula's, we chose arbitrarily the ones without lambda expression and more compact  
    if len(trees) > 1:
        return trees[1]
    else:
        return trees[0]