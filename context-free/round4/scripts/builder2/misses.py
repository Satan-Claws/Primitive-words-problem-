from certs import *
for n in (18,19,20):
    out=[]
    for w in lyndon(n):
        if not (cert_D(w) or cert_GB(w) or cert_RD(w) or cert_RGB(w)): out.append(s(w))
    print(n, out)
g=[s(w) for w in lyndon(12) if not cert_G(w)]
print('G misses n=12:', len(g), g[:12])
