#! /bin/bash
python smt-portfolio.py --z3 "-smt2 -T:5" --cvc5 "--quiet --lang smt --dag-thresh=0 --enum-inst --tlimit 5000"