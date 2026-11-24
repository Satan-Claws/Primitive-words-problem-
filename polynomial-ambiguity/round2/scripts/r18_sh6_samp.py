"""r18_sh6_samp: exact-law sampling of trees of size n in SH6 and EXACT multiplicity m(W) per sampled word
(O(n^2) interval DP, r18_am_lib.count_trees). Usage: r18_sh6_samp.py n1,n2,.. R seed"""
import sys, random, time, threading
import r18_am_lib as L
G = {'tok': [('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','bb'),('a','bb'),('ab','aa')], 'w': 'ab'}
def main():
    ns = [int(x) for x in sys.argv[1].split(',')]; R = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
    S = L.Sampler(G, max(ns))
    for n in ns:
        ms = []; t = time.time()
        for _ in range(R):
            W = S.sample(n, rng); A, _ = L.count_trees(G, W); ms.append(A)
        Em = sum(ms) / R; se = (sum((x - Em) ** 2 for x in ms) / R) ** .5 / R ** .5
        print('n=%5d R=%d E_n[m]=%.3f +- %.3f  P(m>=2)=%.3f  max m=%d  (%.0fs)' % (n, R, Em, se, sum(x >= 2 for x in ms) / R, max(ms), time.time() - t), flush=True)
threading.stack_size(512 * 1024 * 1024); sys.setrecursionlimit(10**6)
th = threading.Thread(target=main); th.start(); th.join()
