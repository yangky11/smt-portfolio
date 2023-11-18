#! /bin/bash
./smt-portfolio.py ex1.smt2 --z3 "-smt2 -T:5" --cvc5 "--quiet --lang smt --dag-thresh=0 --enum-inst --tlimit 5000"