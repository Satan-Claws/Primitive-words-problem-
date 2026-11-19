#!/usr/bin/env python3
"""Independent exhaustive checks for construction.md; no mathematical inference from cutoffs."""
from collections import Counter
from itertools import product


def primitive(word):
    n = len(word)
    return n > 0 and all(word != word[:d] * (n // d) for d in range(1, n) if n % d == 0)


def unbordered(word):
    return bool(word) and all(word[:d] != word[-d:] for d in range(1, len(word)))


def lyndon(word):
    return all(word < word[i:] + word[:i] for i in range(1, len(word)))


def shortest_unique(word):
    n = len(word)
    for k in range(1, n + 1):
        counts = Counter((word + word)[i:i + k] for i in range(n))
        if 1 in counts.values():
            return k
    return None


for i in range(1, 11, 2):
    for j in range(2, 11, 2):
        for k in range(2, 11, 2):
            word = 'a' * i + 'b' + 'a' * j + 'b' + 'a' * k + 'b'
            assert lyndon(word) == (i > j and i > k), (i, j, k)
print('PASS: Lyndon parity slice, 125 triples')

for n in range(1, 15):
    prim_count = 0
    maximum_shortest = 0
    for letters in product('ab', repeat=n):
        word = ''.join(letters)
        if primitive(word):
            prim_count += 1
            minimum = shortest_unique(word)
            assert minimum <= max(1, n // 2), (word, minimum)
            maximum_shortest = max(maximum_shortest, minimum)
        else:
            for split in range(1, n):
                u, v = word[:split], word[split:]
                assert not (u != v and unbordered(u) and unbordered(v)), (u, v)
    print(f'PASS: n={n}, primitive_count={prim_count}, max_shortest_unique={maximum_shortest}')

for s in range(30):
    word = 'a' * (s + 2) + 'b' + 'a' * s + 'b'
    assert primitive(word)
    assert shortest_unique(word) == s + 2
print('PASS: sharp unique-factor family, 30 examples')

context_checks = 0
for total_length in range(1, 9):
    for letters in product('ab', repeat=total_length):
        context = ''.join(letters)
        for split in range(total_length + 1):
            x, y = context[:split], context[split:]
            c = y + x
            z = 'b' + 'a' * (len(c) + 1) + 'b'
            u = z + c + z
            assert primitive(u), (x, y, u)
            assert x + u + y == (x + z + y) * 2
            context_checks += 1
print(f'PASS: universal fixed-context obstruction, {context_checks} contexts')
