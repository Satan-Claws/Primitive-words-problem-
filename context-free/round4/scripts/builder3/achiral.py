import sys
def achiral(s):
    n=len(s); return any(all(s[i]==s[(c-i)%n] for i in range(n)) for c in range(n))
for fn in sys.argv[1:]:
    L=[l.strip() for l in open(fn) if l.strip()]
    print(fn, len(L), 'achiral:', sum(achiral(s) for s in L))
