#!/usr/bin/env python3
import sys
import time
import shlex
import tempfile
import argparse
import subprocess
from enum import Enum
from typing import List
from pathlib import Path
from abc import ABC, abstractmethod


__version__ = "1.0.0"


class Result(Enum):
    SAT = 1
    UNSAT = 2
    UNKNOWN = 3
    TIMEOUT = 4

    def __str__(self) -> str:
        if self == Result.SAT:
            return "sat"
        elif self == Result.UNSAT:
            return "unsat"
        elif self == Result.UNKNOWN:
            return "unknown"
        elif self == Result.TIMEOUT:
            return "timeout"
        else:
            raise ValueError(f"Unexpected result: {self}")


class Solver(ABC):
    def __init__(self, args: str):
        self.args = args

    @abstractmethod
    def run(self, input_file: str) -> Result:
        raise NotImplementedError


class Z3(Solver):
    def run(self, input_file: Path) -> subprocess.Popen:
        return subprocess.Popen(
            shlex.split(f"z3 {self.args} {input_file}"),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            bufsize=1,
        )

    def parse_result(self, out: str, err: str) -> Result:
        if out == "sat":
            return Result.SAT
        elif out == "unsat":
            return Result.UNSAT
        elif out == "timeout":
            return Result.TIMEOUT
        else:
            return Result.UNKNOWN


class CVC5(Solver):
    def run(self, input_file: Path) -> subprocess.Popen:
        return subprocess.Popen(
            shlex.split(f"cvc5 {self.args} {input_file}"),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            bufsize=1,
        )

    def parse_result(self, out: str, err: str) -> Result:
        if out == "sat":
            return Result.SAT
        elif out == "unsat":
            return Result.UNSAT
        elif out == "" and "cvc5 interrupted by timeout" in err:
            return Result.TIMEOUT
        else:
            return Result.UNKNOWN


def clean(procs: List[subprocess.Popen]) -> None:
    for p in procs:
        p.kill()


def run_all(solvers: List[Solver], input_file: Path) -> Result:
    procs = [s.run(input_file) for s in solvers]
    done = [False for _ in solvers]
    results = [None for _ in solvers]

    while not all(done):
        for i, p in enumerate(procs):
            if done[i] or p.poll() is None:
                continue
            done[i] = True
            out = p.stdout.read().strip()
            err = p.stderr.read().strip()
            r = solvers[i].parse_result(out, err)
            results[i] = r
            if r in [Result.SAT, Result.UNSAT]:
                clean(procs)
                return r
        time.sleep(0.01)

    for r in results:
        assert r in [Result.UNKNOWN, Result.TIMEOUT]

    if all(r == Result.TIMEOUT for r in results):
        return Result.TIMEOUT
    else:
        return Result.UNKNOWN


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        type=Path,
        required=False,
        help="Input SMT-LIB file. If `None`, it reads formula from stdin until `(check-sat)`",
    )
    parser.add_argument("--z3", type=str, help="Z3's command line arguments")
    parser.add_argument("--cvc5", type=str, help="CVC5's command line arguments")
    args = parser.parse_args()

    solvers = []
    if args.z3:
        solvers.append(Z3(args.z3))
    if args.cvc5:
        solvers.append(CVC5(args.cvc5))

    if args.file:
        result = run_all(solvers, args.file)
    else:
        oup = tempfile.NamedTemporaryFile("wt")
        for line in sys.stdin:
            oup.write(line)
            if line.strip() == "(check-sat)":
                break
        oup.flush()
        result = run_all(solvers, Path(oup.name))

    print(result)


if __name__ == "__main__":
    main()
