import re
from nltk.sem.logic import ExistsExpression, AndExpression, ApplicationExpression, ConstantExpression, \
    IndividualVariableExpression

"""
Transform a valid FOL formula in a simpleNLG sentence plan
Input:
    s: sentence
    formula: semantic formula of sentence (FOL)
    tree: tree
"""
def getSentencePlan(s, formula, tree):
    print ("FOL: " + str(formula))
    template = getFormulaTemplate(str(formula))
    semTerms = getSemanticTerms(formula.term)

    print ("\nSemantic terms:\n" + str(semTerms) + "\n")

    # ---------------------------------------------
    # ----  TEMPLATE 0
    # ---------------------------------------------
    if template == 0:
        verb_pred = semTerms[-1] # verb predicate
        subj, vobj = transitiveVerbArguments(verb_pred) # subj, obj variable

        obj_occurrency = findOccurencies(tree, semTerms, vobj) # occurrency of vobj in leaf predicates
        
        # obj have N pos_tag, others are modifier
        obj = list(filter(lambda x: 'N' == x['tag'], obj_occurrency))[0]
        verb = match_pred_pos(tree, verb_pred)
        subj = match_pred_pos(tree, subj)

        obj_occurrency.remove(obj)
        if verb in obj_occurrency: # il varbo comparirà sia in obj che in verb (xke è una funzione del tipo f(x,y))
            obj_occurrency.remove(verb)

        print ("\n+++++++++++++++")
        print ("+ verb " + str(verb))
        print ("+ subj " + str(subj))
        print ("+ obj " + str(obj))
        print ("+++++++++++++++")

    # ---------------------------------------------
    # ----  TEMPLATE 1
    # ---------------------------------------------
    elif template == 1 or template == 3:
        variablesVisited = set()

        verb_pred = semTerms[0]

        vsubj = intranstitiveVerbSubj(semTerms, verb_pred) # variable of subject
        subj_occurrency = findOccurencies(tree, semTerms, vsubj) # find predicates in which subj variable is present

        variablesVisited.add(str(verb_pred.args[0])) # str altrimenti esce <EventVariableExpression e> 
        variablesVisited.add(vsubj)

        verb = match_pred_pos(tree, verb_pred)
        subj = list(filter(lambda x: 'N' == x['tag'], subj_occurrency))[0]
        subj_occurrency.remove(subj)

        v_notVisited = getAllVariables(semTerms) - variablesVisited # variables not visited yet
        vcompl = [] # complement variables
        for v in v_notVisited: # for each complement variable
            for occ in findOccurencies(tree, semTerms, v):
                vcompl.append(occ)
                # il complemento comparirà sia in subj che in compl (xke è una funzione del tipo f(x,y))
                # occorre rimuoverla da subj
                if occ in subj_occurrency:
                    subj_occurrency.remove(occ)


        print ("\n+++++++++++++++")
        print ("+ verb " + str(verb))
        print ("+ subj " + str(subj))
        print ("+ compl " + str(vcompl))
        print ("+++++++++++++++")

    # ---------------------------------------------
    # ----  TEMPLATE 2
    # ---------------------------------------------
    elif template == 2:
        variablesVisited = set()

        verb_pred = semTerms[3]
        event = str(verb_pred.args[0])

        mod_verb = findOccurencies(tree, semTerms, event) # predicati in cui compare la variabile del verbo (x)

        variablesVisited.add(event)
        verb = match_pred_pos(tree, verb_pred)

        mod_verb.remove(verb)

        # cerchiamo il soggetto
        vsubj = intranstitiveVerbSubj(semTerms, verb_pred) # variable of subject
        variablesVisited.add(vsubj)
        mod_subj = findOccurencies(tree, semTerms, vsubj)
        subj = list(filter(lambda x: 'N' == x['tag'], mod_subj))[0] # subj is the predicate whose tag is N
        mod_subj.remove(subj)

        v_notVisited = getAllVariables(semTerms) - variablesVisited # variables not visited yet
        vcompl = [] # complement variables
        for v in v_notVisited: # for each complement variable
            for occ in findOccurencies(tree, semTerms, v):
                print (occ)
                vcompl.append(occ)
                # il complemento comparirà sia in verb che in compl (xke è una funzione del tipo f(x,y))
                # occorre rimuoverla da verb
                if occ in mod_verb:
                    mod_verb.remove(occ)
        
        print ("\n+++++++++++++++")
        print ("+ verb " + str(verb))
        print ("+ subj " + str(subj))
        print ("+ compl " + str(vcompl))
        print ("+++++++++++++++")



    """existentials = [e.name for e in getExistentialQuantifier(formula)] # get existential quantifier
    unary = getUnaryRelations(formula)  # get unary relations
    binary = getBinaryRelations(formula)    # get binary relations
    print ("*** existentials" + str(existentials))
    print ("*** unary" + str(unary))
    print ("*** binary" + str(binary))"""
    return s

"""
Detect which template have formula
Input: 
    formula: FOL formula
Output:
    template number
"""
def getFormulaTemplate(formula):
    regularExpr = [
        'exists\\s\\w+.\\(\\w+\\(\\w+\\)\\s\\&\\s(\\w+\\(\\w+\\)\\s&\\s)*\\w+\\(\\w+,\\w+\\)\\)',
        'exists\\s\\w+.\\(exists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\)\\s&\\sexists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\s&\\sexists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\)\\)',
        'exists\\s\\w+.\\((\\w+\\(\\w+\\)\\s&\\s)*\\w+\\(\\w+\\)\\s&\\sexists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\s&\\sexists\\s\\w+.\\(\\w+\\(\\w+,\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\)\\)\\)',
        'exists\\s\\w+.\\(exists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\)\\s&\\sexists\\s\\w+.\\((\\w+\\(\\w+\\)\\s&\\s)*\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\)\\)'
    ]

    for i in range(len(regularExpr)):
        if re.match(regularExpr[i], formula):
            return i
    return None

"""
Allow to calculate all terms of semantic expression
Input:
    term: input term (term of expression)
Output:
    terms: all terms of term (semantic expression)
"""
def getSemanticTerms(term):
    terms = []
    aux_subterms(term, terms)
    return terms

"""
Navigate formula to calculate all terms
Input:
    term: term to evaluate (expression)
    terms: current terms evaluated
"""
def aux_subterms(term, terms):
    # serie di if per differenziare la composizione dell'albero
    if hasattr(term, 'term'):
        aux_subterms(term.term, terms)
    if hasattr(term, 'first'):
        aux_subterms(term.first, terms)
    if hasattr(term, 'second'):
        aux_subterms(term.second, terms)
    elif hasattr(term, 'pred'): # leaf
        if not terms.__contains__(term):  # preserva l'ordine
            terms.append(term) 


"""
Calculate transitive verb arguments
Input:
    verb: node of verb (FOL)
Output:
    argument node 
"""
def transitiveVerbArguments(verb):
    return list(map(lambda x: x.variable.name, verb.args))

"""
Calculate the subj of intransitive verb (must see all tree to detect subj)
Tra tutti i termini della formula, cerco i predicati "agente". In base al template è noto che il primo
sia quello che contiene il soggetto. Inoltre nel predicato agent() il secondo argomento corrisponde alla variabile
del soggetto.
Input:
    terms: semantic predicates of tree
    verb: intransitive verb
Output:
    subj variable
"""
def intranstitiveVerbSubj(terms, verb):
    agent = list(filter(lambda x: x.pred.variable.name == 'agent', terms))[0] # get first "agent" predicates in FOL formula
    subj = agent.args[1].variable.name # subj is the second argument of predicate
    return subj

"""
Calculate all variables of FOL formula
Input:
    terms: FOL terms
Output:
    variables: set of variables
"""
def getAllVariables(terms):
    variables = set()
    for t in terms:
        for a in t.args:
            variables.add(a.variable.name)
    return variables

"""
Find var occurrency in tree 
Input:
    tree: tree parse
    terms: semantic terms (FOL)
    var: variable to find
Output:
    list of leaves containing var
"""
def findOccurencies(tree, terms, var):
    pred = set()
    res = []

    # Cerca tra tutti i predicati se hanno come argomento var
    for t in terms: # for each formula terms
        args = list(map(lambda x: x.variable.name, t.args))
        if var in args:
            pred.add(t)
    
    for p in pred:
        node = match_pred_pos(tree, p)
        if node is not None and not res.__contains__(node):
            res.append(node)

    return res
            
"""
match tra termine semantico e PoS-Tag
Input
    tree: albero
    term: termine semantico
Output:
    nodo con l'informazione del PoS-Tag
"""
def match_pred_pos(tree, term):
    leaves = ['TV', 'IV', 'DTV', 'N', 'JJ', 'PropN', 'Det', 'EX', 'PRP', 'AUX', 'CP', 'ADV'] # POS tag of leaves
    pred_name = term.pred.variable.name if hasattr(term, 'pred') else term # get predicate name

    terminals = [i for i in tree.subtrees()]  # ritorna tutti i possibili sottoalberi

    # re.IGNORECASE: Perform case-insensitive matching
    # group() returns the substring that was matched by the RE
    terminals = list(
        filter(lambda x: re.search("\\'(.*)\\'", str(x.label()).split('\n')[0], re.IGNORECASE).group(1) in leaves,
               terminals))  # adesso in subtrees avrò solo le foglie

    for t in terminals: # for each leaf
        if pred_name == getPredicateLemma(t):
            tag = re.search("\\'(.*)\\'", str(t.label()).split('\n')[0], re.IGNORECASE).group(1)
            node = {'pred': pred_name, 'tag': tag}

            # [*type*, 'NUM', 'SEM', 'TNS', 'GEN']
            if 'NUM' in t.label().keys():
                node['num'] = t.label()['NUM']
            if 'TNS' in t.label().keys():
                node['tns'] = t.label()['TNS']
            if tag in ['N', 'PropN'] and 'GEN' in t.label().keys():
                node['gen'] = t.label()['GEN']
            if 'LOC' in t.label().keys():
                node['loc'] = True
            return node
    return None

"""
Calculate predicate lemma   Es: Given image(x,y) return image
Input:
    term predicate
Output:
    predicate lemma
"""
def getPredicateLemma(term):
    tag = re.search("\\'(.*)\\'", str(term.label()).split('\n')[0], re.IGNORECASE).group(1)
    if tag == 'TV': # Transitive verb
        term = term.label()['SEM'].term
        terms = getSemanticTerms(term)
        #print (tag, term, terms)
        terms = list(map(lambda x: x.argument.term, terms))
    elif tag == 'PRP' and 'PERS' in term.label().keys():
        term = term.label()['SEM'].term
        #print (tag, term, term.argument.variable.name)
        return term.argument.variable.name
    elif tag == 'PRP' and 'LOC' in term.label().keys():
        term = getSemanticTerms(term.label()['SEM'].term)[0]
        #print (tag, term, term.argument.term.second.pred.variable.name)
        return term.argument.term.second.pred.variable.name
    elif tag == 'PropN':
        #print (tag, term.label()['SEM'].term.argument.variable.name)
        return term.label()['SEM'].term.argument.variable.name
    else:
        term = term.label()['SEM'].term
        terms = getSemanticTerms(term)
        #print (tag, term, terms)
    terms = list(map(lambda x: x.pred.variable.name, terms))
    return terms[0] if len(terms) > 0 else None