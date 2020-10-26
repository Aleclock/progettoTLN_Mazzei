
# ENG - ITA translator

## Consegna 

La seguente relazione illustra la realizzazione di un traduttore interlingua da inglese ad italiano. L’esercizio consiste nel parsificare ed interpretare le seguenti frasi inglesi:
- You are imagining things.
- There is a price on my head.
- Your big opportunity is flying out of here.
tradurle e infine costruire, tramite l’API SimpleNLG-it [2], una proposizione sintatticamente corretta.

In particolare, la consegna prevede i seguenti step:
1. Scrivere una grammatica CF con semantica (ispirarsi alla grammatica simple-sem.fcfg,
grammars/book_grammars [4][5]) per le frasi in ingresso e usare NLTK [2] per parsificare;
2. Costruire un sentence planner che per ogni formula logica prodotta dalla grammatica crei un sentence plan
valido per SimpleNLG-it;
3. Usare una lessicalizzazione più semplice possibile per trasformare le costanti e i predicati in parole italiane;
4. Usando la libreria SimpleNLG-IT implementare un realizer che trasformi i sentence plans in frasi italiane
[2].

<br/>

## Risultati

Di seguito i risultati ottenuti:

Frase inglese | Frase italiano
------------ | :------------:
You are imagining things | Tu stai immaginando cose.
There is a price on my head | Prezzo esiste sopra mia testa.
Your big opportunity is flying out of here | Tua opportunità grande sta volando da qui via.
You are imagining my head | Tu stai immaginando testa mia.
<br/>

Come si può notare è presente la coordinazione numerica e del genere. Inoltre, i tempi verbali sono rispettati. In alcuni casi l’ordine delle parole non risulta corretto (*da qui via*).
Da una successiva analisi, il problema riscontrato nell’ordine delle parole sembra derivare da una scelta progettuale secondo la quale la parola out (*via*) risulta essere un modificatore del verbo e per questo motivo viene aggiunta al termine della frase in quanto si utilizza il metodo `addModifier()`.
Eventuali miglioramenti potrebbero risolvere gli errori appena descritti e integrare le seguenti funzionalità:
- Aggiunta dei quantificatori e gestione degli articoli;
- Migliorare la gestione dei modificatori;
- Espandere l’utilizzo del sistema per casi d’uso diversi da quelli richiesti.

<br/>

## Sitografia 

[1] <https://github.com/simplenlg/simplenlg> <br/>
[2] <https://github.com/alexmazzei/SimpleNLG-IT/blob/master/docs/Testsimplenlgit.java> <br/>
[3] <https://www.nltk.org/> <br/>
[4] <https://github.com/nltk/nltk_teach/blob/master/examples/grammars/book_grammars/simple-sem.fcfg> <br/>
[5] <http://www.nltk.org/book/ch10.html> <br/>
[6] <http://www.ling.helsinki.fi/kit/2008s/clt310gen/docs/simplenlg-v37.pdf> <br/>