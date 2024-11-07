Write a python program ff_compute.py to compute the first(X) and follow(X) sets for
all nonterminals X of a given context-free grammar G. The nonterminals are capitals, terminals
are lower case letters, and the empty string is represented as a missing right-hand side. Here is an
example:   
<li>S -> AC</li>
<li>A -> aAb</li>
<li>A -> </li>
<li>C -> C c</li>
</li>C -></>
There is only one production per line (no | separating alternative right-hand sides) and white spaces
are allowed everywhere except inside the symbol ->. Assume the production S'→ S$$ is added to the grammar.  

The program should work as follows, where g.txt contains the grammar in the format mentioned
above and ff.txt contains the first(X) and follow(X) sets:
  
$ python ff_compute.py g.txt ff.txt

The output sets are formatted as follows. For each nonterminal X, the output has three lines
containing, in order, X, first(X), follow(X); each set is presented as a comma-separated list,
sorted alphabetically; the nonterminals are also listed in alphabetical order, with S' appearing first.
For the above example, the output is given below. An empty set is shown as an empty line; see
follow(S') = ∅  

<li>S’</li>
<li>a, c, $$</li>
<li>A</li>
<li>a</li>
<li>b, c, $$</li>
<li>C</li>
<li>c</li>
<li>c, $$</li>
<li>S</li>
<li>a, c</li>
<li>$$</li>
