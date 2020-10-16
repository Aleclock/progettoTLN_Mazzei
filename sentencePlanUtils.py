import re
from nltk.sem.logic import ExistsExpression, AndExpression, ApplicationExpression, ConstantExpression, \
    IndividualVariableExpression

"""
Transform a valid FOL formula in a simpleNLG sentence plan
Input:
    formula: semantic formula of sentence (FOL)
    tree: tree
    lex: lexical dictionary (eng to ita translation)
"""
def getSentencePlan(formula, tree, lex):
    template = getFormulaTemplate(str(formula))
    semTerms = getSemanticTerms(formula.term)

    #print ("Semantic terms: " + str(semTerms))

    plan = {}

    # ---------------------------------------------
    # ----  TEMPLATE 0
    # ----  exists x.(obj(x), verb(subj,x))
    # ---------------------------------------------
    if template == 0:
        verb_pred = semTerms[-1] # verb predicate
        subj, vobj = transitiveVerbArguments(verb_pred) # subj, obj variable

        mod_obj = findOccurencies(tree, semTerms, vobj) # occurrency of vobj in leaf predicates

        
        # obj have N pos_tag, others are modifier
        obj = list(filter(lambda x: 'N' == x['tag'], mod_obj))[0]
        verb = add_pred_pos(tree, verb_pred)
        subj = add_pred_pos(tree, subj)

        # check if exist some verb's modifier
        mod_obj.remove(obj)
        if verb in mod_obj: # There will be 2 occurrencies of vobj (function f(x,y)) 
            mod_obj.remove(verb)


        print ("\n--------------------------------------------------")
        print ("+ verb " + str(verb))
        print ("+ subj " + str(subj))
        print ("+ obj " + str(obj))
        print ("--------------------------------------------------")

        plan = createPlan(subj, verb, obj, {}, None, mod_obj, None)

    # ---------------------------------------------
    # ----  TEMPLATE 1
    # ----  exists x.(exists e.(VP(e),exists z.(subj(x),complement(x,z)))) 
    # ---------------------------------------------
    elif template == 1:
        variablesVisited = set() # Used to identify complements predicates

        verb_pred = semTerms[0]

        vsubj = intransitiveVerbSubj(semTerms, verb_pred) # subject variable
        mod_subj = findOccurencies(tree, semTerms, vsubj) # find predicates in which subj variable is present
        subj = list(filter(lambda x: 'N' == x['tag'], mod_subj))[0]

        verb = add_pred_pos(tree, verb_pred)
        
        mod_subj.remove(subj) # Subject modifier

        # Cast needed because verb_pred.arg type is <EventVariableExpression e> and cannot be used
        variablesVisited.add(str(verb_pred.args[0]))
        variablesVisited.add(vsubj)

        vcompl = getAllVariables(semTerms) - variablesVisited # variables not visited yet (complement variables)
        compl = [] # complement
        for v in vcompl: # for each complement variable
            for occ in findOccurencies(tree, semTerms, v):
                compl.append(occ)
                # There will be more occurrencies of vcompl (function f(x,y)) as subject modifier
                if occ in mod_subj:
                    mod_subj.remove(occ)
        

        print ("\n--------------------------------------------------")
        print ("+ verb " + str(verb))
        print ("+ subj " + str(subj))
        print ("+ compl " + str(compl))
        print ("--------------------------------------------------")

        plan = createPlan(subj, verb, {}, compl, mod_subj, None, None)

    # ---------------------------------------------
    # ----  TEMPLATE 2
    # ----  exists x.(subj(x),exists e.(VP(e),exists y.(Pred(e,y))))
    # ---------------------------------------------
    elif template == 2:
        variablesVisited = set()

        verb_pred = semTerms[3]
        event = str(verb_pred.args[0])

        mod_verb = findOccurencies(tree, semTerms, event) # predicates with event as argument
        variablesVisited.add(event)
        
        verb = add_pred_pos(tree, verb_pred)
        mod_verb.remove(verb)

        # Find the subject
        vsubj = intransitiveVerbSubj(semTerms, verb_pred) # variable of subject
        variablesVisited.add(vsubj)
        mod_subj = findOccurencies(tree, semTerms, vsubj)
        subj = list(filter(lambda x: 'N' == x['tag'], mod_subj))[0] # subj is the predicate whose tag is N
        mod_subj.remove(subj)

        vcompl = getAllVariables(semTerms) - variablesVisited # variables not visited yet (complement variables)
        compl = [] # complement predicates
        for v in vcompl: # for each complement variable
            for occ in findOccurencies(tree, semTerms, v):
                compl.append(occ)
                # There will be more occurrencies of vcompl (function f(x,y)) 
                if occ in mod_verb:
                    mod_verb.remove(occ)
        
        
        print ("\n--------------------------------------------------")
        print ("+ verb " + str(verb))
        print ("+ subj " + str(subj))
        print ("+ compl " + str(compl))
        print ("--------------------------------------------------")

        plan = createPlan(subj, verb, {}, compl, mod_subj, mod_verb, None)
       
    return translatePlan(lex, plan)



"""
Translate given arguments using lex dictionary
Input:
    lex: lexical dictionary (eng to ita translation)
    plan: plan to translate ("pred" attributes)
Output:
    translated plan
"""
def translatePlan(lex, plan):
    for p in plan:
        if plan[p]:
            if type(plan[p]) is list: # like complement
                for x in plan[p]:
                    index = plan[p].index(x)
                    plan[p][index]["pred"] = lex[x["pred"]]
            else:
                plan[p]["pred"] = lex[plan[p]["pred"]]

            # translating modifier
            if "mod" in plan[p]:
                for mod in plan[p]["mod"]:
                    index = plan[p]["mod"].index(mod)
                    plan[p]["mod"][index]["pred"] = lex[mod["pred"]]
    return plan


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
        'exists\\s\\w+.\\(exists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\)\\s&\\sexists\\s\\w+.\\((\\w+\\(\\w+\\)\\s&\\s)*\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\)\\)',
        'exists\\s\\w+.\\((\\w+\\(\\w+\\)\\s&\\s)*\\w+\\(\\w+\\)\\s&\\sexists\\s\\w+.\\(\\w+\\(\\w+\\)\\s&\\s\\w+\\(\\w+,\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\s&\\sexists\\s\\w+.\\(\\w+\\(\\w+,\\w+\\)\\s&\\s\\w+\\(\\w+\\)\\)\\)\\)'
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
    # Analyze each part of tree formula
    if hasattr(term, 'term'):
        aux_subterms(term.term, terms)
    if hasattr(term, 'first'):
        aux_subterms(term.first, terms)
    if hasattr(term, 'second'):
        aux_subterms(term.second, terms)
    elif hasattr(term, 'pred'): # leaf
        if not terms.__contains__(term):  # order preserving
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
For each semantic term identifies "agent" predicates. The first one contains subject variable as second argument.
Input:
    terms: semantic predicates of tree
    verb: intransitive verb
Output:
    subj variable
"""
def intransitiveVerbSubj(terms, verb):
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

    # Find all predicates with "var" as argument
    for t in terms: # for each formula terms
        args = set(map(lambda x: x.variable.name, t.args))
        if var in args:
            pred.add(t)
    
    # Add features to predicates
    for p in pred:
        node = add_pred_pos(tree, p)
        if node is not None and not res.__contains__(node):
            res.append(node)

    return res
            
"""
Join semantic term with its pos-tag info
Input
    tree: Tree
    term: semantic term
Output:
    dict with features (pos-tag info)
"""
def add_pred_pos(tree, term):
    leaves = ['TV', 'IV', 'DTV', 'N', 'JJ', 'PropN', 'Det', 'EX', 'PRP', 'AUX', 'CP', 'ADV'] # POS tag of leaves
    pred_name = term.pred.variable.name if hasattr(term, 'pred') else term # get predicate name

    terminals = [i for i in tree.subtrees()]  # return all the possible subtrees

    terminals = list(
        filter(lambda x: re.search("\\'(.*)\\'", str(x.label()).split('\n')[0], re.IGNORECASE).group(1) in leaves,
               terminals))  # filter terminals keeping only the leaves

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
        terms = list(map(lambda x: x.argument.term, terms))
    elif tag == 'PRP' and 'PERS' in term.label().keys():
        term = term.label()['SEM'].term
        return term.argument.variable.name
    elif tag == 'PRP' and 'LOC' in term.label().keys():
        term = getSemanticTerms(term.label()['SEM'].term)[0]
        return term.argument.term.second.pred.variable.name
    elif tag == 'PropN':
        return term.label()['SEM'].term.argument.variable.name
    else:
        term = term.label()['SEM'].term
        terms = getSemanticTerms(term)
    terms = list(map(lambda x: x.pred.variable.name, terms))
    return terms[0] if len(terms) > 0 else None


"""
Create a dictionary containing semantic parts of the sentence
Input:
    subj: subject dictionary
    z
"""
def createPlan(subj, verb, obj, compl, mod_subj, mod_verb, mod_compl):
    plan = {}

    plan["subj"] = subj
    plan["verb"] = verb
    plan["obj"] = obj
    plan["compl"] = compl

    if mod_subj:
        plan["subj"]["mod"] = mod_subj
    if mod_verb:
        plan["verb"]["mod"] = mod_verb
    if mod_compl: 
        plan["compl"]["mod"] = mod_compl
    
    return plan