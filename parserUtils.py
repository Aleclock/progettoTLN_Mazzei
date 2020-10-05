import nltk
from nltk import load_parser

"""
grammar (simple-sem.fcfg) contains a small set of rules for parsing and translating simple examples of the kind that we have been looking at.
"""
def parseSentence(sentence, grammar):
    parser = load_parser(grammar, trace=0)
    trees = list(parser.parse(sentence.split()))

    # TODO cercare un modo decente per farlo (il tipo lo fa con la funzione bestTree())
    if len(trees) > 1:
        return trees[1]
    else:
        return trees[0]