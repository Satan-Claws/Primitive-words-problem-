"""numerics for (AM): exact enumeration (n<=K) and exact-law sampling (large n) of the exit-slide multiplicity
m(W) in critical IF-clean heavy-tailed single linear SCCs (Dyck block B, tail k^{-3/2}, beta0=1/2)."""
import random, sys, math
import r18_am_lib as L
EX = {
 'SH3': ({'tok':[('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('a','bb'),('ab','bb')],'w':'ab'}),
 'SH4': ({'tok':[('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('a','bbb'),('b','bb')],'w':'ab'}),
 'SH5': ({'tok':[('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('b','bb'),('ba','bb')],'w':'ab'}),
 'SH6': ({'tok':[('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','bb'),('a','bb'),('ab','aa')],'w':'ab'}),
 'SH1': ({'tok':[('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('','bbb'),('a','baa')],'w':'ab'}),
 'SH2': ({'tok':[('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('','bbb'),('','bbaa')],'w':'ab'}),
 'H1': ({'tok':[('B',''),('b','b'),('b','aa'),('aa','aaa'),('ba','baa'),('ba','ba')],'w':'b'}),
 'H2': ({'tok':[('','B'),('baa','b'),('aba','aab'),('a','abb'),('ab','bab'),('abb','bab'),('aab','b'),('','baa'),('bbb','b'),('bbb','aba'),('aaa','bba'),('bab','aab'),('aba','bba')],'w':'ba'}),
 'H3': ({'tok':[('B',''),('aab','bba'),('b','baa'),('baa','bbb'),('b','aa'),('ba','bba'),('ba','aab'),('aa','ba'),('bbb','aab'),('ba','ab'),('aa','aaa'),('bbb','aba'),('bab','bba'),('bab','abb')],'w':'a'}),
}
name = sys.argv[1]; G = EX[name]; mode = sys.argv[2]
if mode == 'if':
    print(name, 'IF violations to len', sys.argv[3], ':', L.check_IF(G, int(sys.argv[3])))
elif mode == 'enum':
    K = int(sys.argv[3]); words = L.enumerate_trees(G, K); u, D0, Em, nw = L.stats_from_enum(words, K)
    S0 = 0; U = 0; Wm = 0
    for k in range(K + 1):
        S0 += D0[k]; U += u[k]; Wm += nw[k]
        if k % 2 == 0 and k >= 8: print('k=%2d u=%.4f E_k[m]=%.3f S0=%.4f U=%.3f wordmass=%.3f U/(1+S0)=%.3f' % (k, u[k], Em[k], S0, U, Wm, U/(1+S0)))
elif mode == 'samp':
    ns = [int(x) for x in sys.argv[3].split(',')]; R = int(sys.argv[4]); rng = random.Random(7)
    S = L.Sampler(G, max(ns))
    for n in ns:
        ms = []; d0 = []
        for _ in range(R):
            W = S.sample(n, rng); A, first = L.count_trees(G, W)
            ms.append(A)
        Em = sum(ms) / R; se = (sum((x - Em) ** 2 for x in ms) / R) ** .5 / R ** .5
        print('n=%4d E_n[m]=%.3f +- %.3f  P(m>=2)=%.3f  max m=%d' % (n, Em, se, sum(x >= 2 for x in ms) / R, max(ms)), flush=True)
