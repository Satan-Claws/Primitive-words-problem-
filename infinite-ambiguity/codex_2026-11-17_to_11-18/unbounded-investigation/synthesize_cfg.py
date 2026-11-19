#!/usr/bin/env python3
"""Bounded-example CNF synthesis. Finite evidence only; never certifies Q.

All rules A->BC and A->a/b are available, including start on RHS.
For each tested word, membership is encoded exactly by CYK Boolean recurrences.
The outer loop adds counterexamples from exhaustive words through max_length.
"""
import argparse
import itertools
import json
import time
from pathlib import Path

import z3


def primitive(w):
    return bool(w) and all(w != w[:d] * (len(w) // d)
                           for d in range(1, len(w)) if len(w) % d == 0)


def run(k, max_length, seconds, destination):
    started = time.monotonic()
    solver = z3.Solver()
    terminal = [[z3.Bool(f't_{a}_{c}') for c in range(2)] for a in range(k)]
    binary = [[[z3.Bool(f'p_{a}_{b}_{c}') for c in range(k)]
               for b in range(k)] for a in range(k)]
    membership = {}
    examples = set()
    history = []

    def symbolic(w):
        if w in membership:
            return membership[w]
        values = [z3.Bool(f'm_{a}_{w}') for a in range(k)]
        membership[w] = values
        if len(w) == 1:
            for a in range(k):
                solver.add(values[a] == terminal[a]['ab'.index(w)])
        else:
            splits = [(symbolic(w[:i]), symbolic(w[i:])) for i in range(1, len(w))]
            for a in range(k):
                solver.add(values[a] == z3.Or([
                    z3.And(binary[a][b][c], left[b], right[c])
                    for left, right in splits for b in range(k) for c in range(k)]))
        return values

    def add_example(w):
        if w not in examples:
            examples.add(w)
            solver.add(symbolic(w)[0] == primitive(w))

    for w in ('a', 'b', 'aa', 'bb', 'ab', 'ba', 'aaa', 'bbb', 'aba', 'bab'):
        add_example(w)

    round_number = 0
    candidate = None
    outcome = 'timeout'
    while time.monotonic() - started < seconds:
        round_number += 1
        remaining = seconds - (time.monotonic() - started)
        solver.set(timeout=max(1, int(min(remaining, 60) * 1000)))
        result = solver.check()
        if result == z3.unsat:
            outcome = 'unsat_on_finite_examples'
            break
        if result == z3.unknown:
            print(json.dumps({'k': k, 'round': round_number, 'result': 'unknown',
                              'reason': solver.reason_unknown(), 'examples': len(examples)}), flush=True)
            continue
        model = solver.model()
        terminals = [[bool(z3.is_true(model.eval(v, model_completion=True))) for v in row]
                     for row in terminal]
        rules = [(a, b, c) for a in range(k) for b in range(k) for c in range(k)
                 if z3.is_true(model.eval(binary[a][b][c], model_completion=True))]
        lookup = [[0] * k for _ in range(k)]
        for a, b, c in rules:
            lookup[b][c] |= 1 << a
        masks = {letter: sum((1 << a) for a in range(k) if terminals[a][i])
                 for i, letter in enumerate('ab')}
        bad = []
        first_bad_length = None
        checked = 0
        for n in range(1, max_length + 1):
            for letters in itertools.product('ab', repeat=n):
                w = ''.join(letters)
                if n > 1:
                    value = 0
                    for i in range(1, n):
                        left, right = masks[w[:i]], masks[w[i:]]
                        for b in range(k):
                            if left & (1 << b):
                                for c in range(k):
                                    if right & (1 << c):
                                        value |= lookup[b][c]
                    masks[w] = value
                checked += 1
                if bool(masks[w] & 1) != primitive(w):
                    if first_bad_length is None:
                        first_bad_length = n
                    if len(bad) < 32:
                        bad.append(w)
            if first_bad_length is not None:
                break
        candidate = {'terminals': terminals, 'binary_rules': rules}
        event = {'round': round_number, 'examples': len(examples), 'checked': checked,
                 'first_bad_length': first_bad_length, 'counterexamples': bad,
                 'rules': len(rules), 'elapsed': round(time.monotonic() - started, 3)}
        history.append(event)
        print(json.dumps(dict(k=k, **event)), flush=True)
        if not bad:
            outcome = 'matches_through_bound_only'
            break
        for w in bad:
            add_example(w)
    output = {'k': k, 'max_length': max_length, 'outcome': outcome,
              'elapsed_seconds': time.monotonic() - started,
              'examples': sorted(examples, key=lambda w: (len(w), w)),
              'last_candidate': candidate,
              'last_candidate_status': ('matches_through_bound_only' if outcome == 'matches_through_bound_only'
                                        else 'rejected_or_stale_not_a_solution'),
              'history': history}
    destination.write_text(json.dumps(output, indent=2) + '\n')
    destination.with_suffix('.smt2').write_text(solver.to_smt2())
    print(json.dumps({key: output[key] for key in ('k', 'outcome', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nonterminals', type=int, required=True)
    parser.add_argument('--max-length', type=int, default=12)
    parser.add_argument('--seconds', type=int, default=600)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.nonterminals, args.max_length, args.seconds, args.output)
