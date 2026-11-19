"""Exact finite experiments; none constitutes an asymptotic CFL proof."""
import argparse
import itertools
import json
from pathlib import Path


def primitive(w):
    return bool(w) and all(w != w[:d] * (len(w) // d)
                           for d in range(1, len(w)) if len(w) % d == 0)


def prime_divisors(n):
    return [p for p in range(2, n + 1)
            if n % p == 0 and all(p % d for d in range(2, int(p ** .5) + 1))]


def enumerate_counts(limit):
    result = []
    for n in range(1, limit + 1):
        checks = [(n // p, ((1 << n) - 1) // ((1 << (n // p)) - 1))
                  for p in prime_divisors(n)]
        q = sum(all(x != (x & ((1 << d) - 1)) * multiplier
                    for d, multiplier in checks) for x in range(1 << n))
        # Independent recurrence from unique primitive roots.
        expected = (1 << n) - sum(row['primitive'] for row in result
                                 if n % row['length'] == 0)
        assert q == expected, (n, q, expected)
        result.append({'length': n, 'primitive': q, 'nonprimitive': (1 << n) - q})
    return result


def minimum_cnf(n, max_k=12, timeout_ms=60000):
    """Minimize nonterminals in strict epsilon-free CNF for Q up to length n.

    Finite-language reduced CNF grammars are acyclic: a dependency cycle
    adds at least one productive sibling at each step and hence pumps length.
    Therefore topologically ordered nonterminals lose no optimal grammar.
    Integer height bounds prohibit ALL words longer than n, not just tested
    words. Boolean membership equations cover every word of length <= n.
    """
    import z3
    words = [''.join(x) for length in range(1, n + 1)
             for x in itertools.product('ab', repeat=length)]
    trials = []
    for k in range(1, max_k + 1):
        solver = z3.Solver()
        solver.set(timeout=timeout_ms)
        terminal = {(a, c): z3.Bool(f't_{a}_{c}') for a in range(k) for c in 'ab'}
        binary = {(a, b, c): z3.Bool(f'r_{a}_{b}_{c}')
                  for a in range(k) for b in range(a) for c in range(a)}
        derives = {(a, w): z3.Bool(f'd_{a}_{w}') for a in range(k) for w in words}
        maximum = [z3.Int(f'max_{a}') for a in range(k)]
        for a in range(k):
            solver.add(maximum[a] >= 1, maximum[a] <= n)
            solver.add(z3.Or([terminal[a, c] for c in 'ab'] +
                             [binary[a, b, c] for b in range(a) for c in range(a)]))
            for b in range(a):
                for c in range(a):
                    solver.add(z3.Implies(binary[a, b, c], maximum[a] >= maximum[b] + maximum[c]))
            for w in words:
                rhs = terminal[a, w] if len(w) == 1 else z3.Or([
                    z3.And(binary[a, b, c], derives[b, w[:i]], derives[c, w[i:]])
                    for b in range(a) for c in range(a) for i in range(1, len(w))])
                solver.add(derives[a, w] == rhs)
        for w in words:
            solver.add(derives[k - 1, w] == primitive(w))
        answer = solver.check()
        trials.append({'nonterminals': k, 'result': str(answer)})
        if answer == z3.unknown:
            return {'max_length': n, 'trials': trials, 'minimum': None, 'reason': solver.reason_unknown()}
        if answer == z3.sat:
            model = solver.model()
            rules = []
            languages = []
            for a in range(k):
                language = set()
                for c in 'ab':
                    if z3.is_true(model.eval(terminal[a, c])):
                        rules.append([a, c]); language.add(c)
                for b in range(a):
                    for c in range(a):
                        if z3.is_true(model.eval(binary[a, b, c])):
                            rules.append([a, [b, c]])
                            language.update(x + y for x in languages[b] for y in languages[c])
                languages.append(language)
            assert languages[-1] == {w for w in words if primitive(w)}
            return {'max_length': n, 'trials': trials, 'minimum': k,
                    'start': k - 1, 'rules': rules,
                    'verification': 'Independent complete acyclic-language expansion'}
    return {'max_length': n, 'trials': trials, 'minimum': None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['count', 'cnf'])
    parser.add_argument('--limit', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.mode == 'count':
        result = enumerate_counts(args.limit)
        print(json.dumps(result, indent=2), flush=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    else:
        result = []
        for n in range(1, args.limit + 1):
            row = minimum_cnf(n)
            result.append(row)
            args.output.write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps(row), flush=True)
            if row['minimum'] is None:
                break
