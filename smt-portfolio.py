import argparse
from abc import ABC, abstractmethod


class Solver(ABC):
    def __init__(self, args: str):
        self.args = args


class Z3(Solver):
    pass


class CVC5(Solver):
    pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("iput-file", type=str, help="Input SMT-LIB file")
    parser.add_argument("--z3", type=str, help="Z3's command line arguments")
    parser.add_argument("--cvc5", type=str, help="CVC5's command line arguments")
    args = parser.parse_args()
    print(args)

    solvers = []
    if args.z3:
        solvers.append(Z3(args.z3))
    if args.cvc5:
        solvers.append(CVC5(args.cvc5))


if __name__ == "__main__":
    main()
