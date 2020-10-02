from nltk import load_parser

"""
grammar (simple-sem.fcfg) contains a small set of rules for parsing and translating simple examples of the kind that we have been looking at.
"""
def parseSentence(sentence, grammar):
    parser = load_parser(grammar, trace=0)
    trees = list(parser.parse(sentence.split()))
    for tree in trees:
        print(tree.label()['SEM'])
        """
        http://www.nltk.org/book/ch10.html
        The "reduction" of (36) to (37) is an extremely useful operation in simplifying semantic representations, and we shall use it a lot in the rest of this chapter. 
        The operation is often called β-reduction. In order for it to be semantically justified, we want it to hold that λx. α(β) has the same semantic values as α[β/x]. 
        This is indeed true, subject to a slight complication that we will come to shortly. In order to carry of β-reduction of expressions in NLTK, 
        we can call the simplify() method
        """
        #print(tree.label()['SEM'].simplify())
    return trees[0]