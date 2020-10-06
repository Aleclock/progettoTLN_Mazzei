
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

quindi il verbo corrisponde all'ultimo predicato della formula. Sapendo che il verbo è transitivo, gli argomenti del verbo vengono determinati con la funzione `transitiveVerbArguments()`, la quale ritorna la lista dei nomi degli argomenti del predicato corrispondente al verbo. Mentre l'argomento soggetto (`sobj`) risulta essere il nome del predicato, l'argomento dell'oggetto è una variabile. Per questo motivo risulta necessario cercare tra tutti i predicati della formula quelli che contengono la variabile `vobj` (funzione `findOccurencies()`).

La funzione `findOccurencies()` cerca seleziona, tra tutti i predicati della formula, quelli che hanno come argomenti la variabile da cercare (`var`). Sucecssivamente per ogni predicato contenente l'oggetto, viene fatto un matching tra il predicato e il corrispondente part-of-speech tag. Quest'ultima operazione viene fatta con la funzione `match_pred_pos()`, la quale inizialmente determina il nome del predicato e poi calcola tutti i possibili alberi dell'albero sintattico iniziale (`tree.subtrees()`). Tra tutti i possibili sotto-alberi, vengono selezionati solo quelli che corrispondono alle foglie (attraverso una ricerca sulle espressioni regolari)

```python
terminals = list(filter(
    lambda x: re.search("\\'(.*)\\'", str(x.label()).split('\n')[0], re.IGNORECASE).group(1) in leaves, terminals)) 
```

Per ogni foglia, nel caso in cui il nome del predicato corrisponda al lemma del predicato foglia, viene creato un dizionario contenente alcune informazioni relative alla sintassi e alla semantica (nome del predicato, pos tag, numero, genere, locativo).

<br/>

Siccome l'oggetto di un verbo ha come POS tag `N` (*nome*), tra la lista di predicati contenenti la variabile oggetto (`vobj`) viene selezionato solo quello il cui TAG corrisponde al nome. Infine si determinano, come fatto con l'oggetto, le informazioni sintattiche del verbo e del soggetto attraverso la funzione `match_pred_pos()`.

<br/><br/>

### **Template 1**

Il template 1 è del tipo

```
exists x.(exists e.(VP(e), exists z.(subj(x), complement(x,z))))
```

quindi il verbo corrisponde al primo predicato della formula. Sapendo che il verbo è intransitivo, il soggetto viene determinato con la funzione `intranstitiveVerbSubj()`, la quale determina la variabile associata al soggetto. Questa funzione seleziona tra i termini semantici della formula il predicato il cui nome è "agent". Il predicato corrispondente al soggetto risulta essere il primo predicato "agent" nella formula. Per determinare il nome del predicato associato al soggetto è necessario cercare tra tutti i predicati della formula quelli che contengono la variabile `vsubj` tramite la funzione `findOccurencies()`. Il predicato corrispondente al soggetto risulta essere quello il cui tag sintattico corrisponde a *Noun*.
Dopo aver determinato il verbo e il soggetto, si ottengono le rispettive informazini sintattiche attraverso la funzione `match_pred_pos()`.

Per determinare il predicato corrispondente al complemento, si calcolano inizialmente tutte le variabili presenti nella formula (funzione `getAllVariables()`). Dalla lista totale delle variabili vengono rimosse quelle corrispondenti al verbo e al soggetto. Avendo determinato la variabile del complemento, è possibile determinare tutti i predicati in cui la variabile compare (attraverso `findOccurencies()`)

<br/><br/>

### **Template 2**

Il template 2 è del tipo

```
exists x.(subj(x), exists e.(VP(e), exists y.(Pred(e,y))))
```

quindi il verbo corrisponde al quarto predicato della formula. Sapendo che il verbo è intransitivo, il soggetto viene determinato con la funzione `intranstitiveVerbSubj()`, la quale determina la variabile associata al soggetto. Questa funzione seleziona tra i termini semantici della formula il predicato il cui nome è "agent". Il predicato corrispondente al soggetto risulta essere il primo predicato "agent" nella formula. Per determinare il nome del predicato associato al soggetto è necessario cercare tra tutti i predicati della formula quelli che contengono la variabile `vsubj` tramite la funzione `findOccurencies()`. Il predicato corrispondente al soggetto risulta essere quello il cui tag sintattico corrisponde a *Noun*.

Dopo aver determinato il verbo e il soggetto, si ottengono le rispettive informazini sintattiche attraverso la funzione `match_pred_pos()`.

Come nel caso precedente (template 1), vengono determinate tutte le variabili presenti nella formula (`getAllVariables()`) e, tra queste, vengono rimosse quelle corrispondenti al verbo e al soggetto. La variabile rimanente corrisponde al complemento e quindi vengono calcolati tutti i predicati contententi la variabile (`findOccurencies()`).

<br/><br/>

In base alle tre frasi in input, il risultato di questa fase è il seguente:

```
Sentence: you are imagining things
FOL: exists z2.(thing(z2) & image(you,z2))

verb {'pred': 'image', 'tag': 'TV', 'num': 'sg', 'tns': 'ger'}
subj {'pred': 'you', 'tag': 'PRP', 'num': 'sg'}
obj {'pred': 'thing', 'tag': 'N', 'num': 'pl', 'gen': 'f'}
```

```
Sentence: there is a price on my head
FOL: exists x.(exists e.(presence(e) & agent(e,x)) & exists z5.(my(z5) & head(z5) & price(x) & on(x,z5)))

verb {'pred': 'presence', 'tag': 'IV', 'num': 'sg', 'tns': 'pres'}
subj {'pred': 'price', 'tag': 'N', 'num': 'sg', 'gen': 'f'}
compl [
    {'pred': 'head', 'tag': 'N', 'num': 'sg', 'gen': 'f'}, 
    {'pred': 'on', 'tag': 'PRP', 'loc': True}, {'pred': 'my', 'tag': 'JJ', 'num': 'sg'}]
```

```
Sentence: your big opportunity is flying out of here
FOL: exists x.(your(x) & big(x) & opportunity(x) & exists e.(fly(e) & agent(e,x) & out(e) & exists y.(from(e,y) & here(y))))

verb {'pred': 'fly', 'tag': 'IV', 'num': 'sg', 'tns': 'ger'}
subj {'pred': 'opportunity', 'tag': 'N', 'num': 'sg', 'gen': 'f'}
compl [{'pred': 'here', 'tag': 'N', 'num': 'sg', 'gen': 'm', 'loc': True}, {'pred': 'from', 'tag': 'PRP'}]
```

<br/><br/>

## 3. Sentence plan to translation

<br/><br/>