# smt-portfolio

A simple wrapper to run multiple SMT solvers in parallel (currently supporting Z3 and CVC5).

[![PyPI](https://img.shields.io/pypi/v/smt-portfolio)](https://pypi.org/project/smt-portfolio/) [![GitHub license](https://img.shields.io/github/license/yangky11/smt-portfolio)](https://github.com/yangky11/smt-portfolio/blob/main/LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 

______________________________________________________________________


## Requirements

* Z3
* CVC5
* Vampire

## Installation

```bash
pip install smt-portfolio
```

## Usage

```bash
smt-portfolio --help
```

```bash
smt-portfolio --file examples/ex1.smt2 --z3 "-smt2 -T:5" --cvc5 "--quiet --lang smt --dag-thresh=0 --enum-inst --tlimit 5000" --vampire "--input_syntax smtlib2 --output_mode smtcomp --time_limit 5"
cat examples/ex1.smt2 | smt-portfolio --z3 "-smt2 -T:5" --cvc5 "--quiet --lang smt --dag-thresh=0 --enum-inst --tlimit 5000" --vampire "--input_syntax smtlib2 --output_mode smtcomp --time_limit 5"
```
