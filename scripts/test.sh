#! /bin/bash
smt-portfolio --file examples/ex1.smt2 --z3 "-smt2 -T:5" --cvc5 "--quiet --lang smt --dag-thresh=0 --enum-inst --tlimit 5000"
cat examples/ex1.smt2 | smt-portfolio --z3 "-smt2 -T:5" --cvc5 "--quiet --lang smt --dag-thresh=0 --enum-inst --tlimit 5000"