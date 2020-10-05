
# ENG - ITA translator

## 0. Load sentences

Le frasi, presenti nel file *sentences.txt*, sono le seguenti:

* You are imagining things
* There is a price on my head
* Your big opportunity is flying out of here

<br/><br/>

## 1. Parse sentence and grammar

<br/><br/>

## 2. Formula to sentence plan

Dopo aver effettuato il parsing della frase in input, è necessario effettuare il sentence plan. In base alla rappresentazione semantica delle frasi proposte, è possibile categorizzarle in tre classi:

* `exists x.(obj(x), verb(subj,x))`, frase dichiarativa con soggetto, verbo (transitivo) e oggetto (diretto)
* `exists x.(exists e.(VP(e), exists z.(subj(x), complement(x,z))))`, frase con un complemento che mette in relazione il soggetto con qualcosa (un generico NP)
* `exists x.(subj(x), exists e.(VP(e), exists y.(Pred(e,y))))`, frase con soggetto, verbo e predicato che mette in relazione il verbo con qualcosa (un generico NP).

<br/>

In base al template della formula, è possibile determinare gli elementi della frase. <br/>

La funzione `getSentencePlan()` prende in ingresso:

* `s`: frase da tradurre;
* `formula`: formula semantica FOL;
* `tree`: albero sintattico.

Inizialmente viene dedotto il template della frase con la funzione `getFormulaTemplate()`, la quale effettua un'operazione di matching tra la formula e l'espressione regolare. Inoltre vengono calcolati tutti i predicati che compongono la formula. La funzione `getSemanticTerms()` effettua una ricerca ricorsiva tra gli elementi della formula. 

```python
def aux_subterms(term, terms):
    if hasattr(term, 'term'):
        aux_subterms(term.term, terms)
    if hasattr(term, 'first'):
        aux_subterms(term.first, terms)
    if hasattr(term, 'second'):
        aux_subterms(term.second, terms)
    elif hasattr(term, 'pred'): # leaf
        if not terms.__contains__(term):
            terms.append(term) 
```

In particolare nel caso in cui il termine sia un esistenziale (*ExistsExpression*) viene fatta nuovamente la ricerca sui suoi termini (`term.term`). Nel caso in cui il termine sia un'espressione And (*AndExpression*) e quindi siano presenti gli attributi `first` e `second`, viene fatta la ricerca sui corrispondenti elementi. Infine nel caso in cui il termine abbia un attributo `pred`, ovvero nel caso in cui si tratti di una foglia, il termine viene aggiunto alla lista dei predicati della formula.

<br/>

In base al template della formula il procedimento si divide, in modo tale da determinare correttamente gli argomenti (soggetto, verbo e complemento/oggetto).

<br/><br/>

### **Template 0**

Il template 0 è del tipo

```
exists x.(obj(x), verb(subj,x))
```

quindi il verbo corrisponde all'ultimo predicato della formula. Sapendo che il verbo è transitivo, gli argomenti del verbo vengono determinati con la funzione `transitiveVerbArguments()`, la quale ritorna la lista dei nomi degli argomenti del predicato corrispondente al verbo. Mentre l'argomento soggetto (`sobj`) risulta essere il nome del predicato, l'argomento dell'oggetto è una variabile. Per questo motivo risulta necessario cercare tra tutti i predicati della formula quelli che contengono la variabile `obj` (funzione `findOccurencies()`).

La funzione `findOccurencies()` cerca seleziona, tra tutti i predicati della formula, quelli che hanno come argomenti la variabile da cercare (`var`). Sucecssivamente per ogni predicato contenente l'oggetto, viene fatto un matching tra il predicato e il corrispondente part-of-speech tag. Quest'ultima operazione viene fatta con la funzione `match_pred_pos()`, la quale inizialmente determina il nome del predicato e poi calcola tutti i possibili alberi dell'albero sintattico iniziale (`tree.subtrees()`). Tra tutti i possibili sotto-alberi, vengono selezionati solo quelli che corrispondono alle foglie (attraverso una ricerca sulle espressioni regolari)

```python
terminals = list(filter(
    lambda x: re.search("\\'(.*)\\'", str(x.label()).split('\n')[0], re.IGNORECASE).group(1) in leaves, terminals)) 
```

Per ogni foglia, nel caso in cui il nome del predicato corrisponda al lemma del predicato foglia, viene creato un dizionario contenente alcune informazioni relative alla sintassi e alla semantica.

<br/><br/>

## 3. Sentence plan to translation

<br/><br/>