import sys
import fine_nc as M
# coords given explicitly: fine coordinate list of coarse block indices (0..n-1), in word order
def run(coords,k):
    n=max(coords)+1
    M.setup=lambda n_,parts: coords
    return M.run(n,None,'MET',k)
if __name__=='__main__':
    coords=[int(x) for x in sys.argv[1].split(',')]; k=int(sys.argv[2])
    ok,t,tot,fam=run(coords,k)
    print('coords',coords,'k',k,'structures',tot,'coverer wins after %d'%t if ok else 'ATTACKER SURVIVES')
    if not ok:
        for U in list(fam.values())[:3]: print(' dim',len(U.basis),[[x if x<M.P//2 else x-M.P for x in v] for v in U.basis][:4])
