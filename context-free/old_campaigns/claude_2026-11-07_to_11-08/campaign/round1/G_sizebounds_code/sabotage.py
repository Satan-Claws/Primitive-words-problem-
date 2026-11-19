# Falsification controls: shrink the window below the Fine-Wilf threshold and see completeness fail.
import numpy as np
from cover_verify import *
for n in [12, 18, 20, 24]:
    D, E, M1, M2, lam0, s0 = params(n)
    print("n",n,"M1+M2",M1+M2,"default lam",lam0)
    for lam in range(lam0, max(M1,1), -1):
        # force spacing 1 (all n windows) to isolate the length condition
        words = np.arange(1 << n, dtype=np.int64)
        prim = primitive_mask(words, n)
        cov = np.zeros(len(words), bool)
        wmask = (1 << lam) - 1
        h = n//2
        for t in range(n):
            x = rot(words, t, n) & wmask
            perE = np.zeros(len(words), bool)
            for d in E:
                perE |= has_period(x, lam, d) if d < lam else True
            aE = ~perE
            if n % 2:
                cov |= aE
            else:
                if h < lam: cov |= aE & ~has_period(x, lam, h)
                for o in range(lam):
                    i=(t+o)%n; j=(i+h)%n
                    if (j-t)%n < lam: continue
                    cov |= aE & (((words>>i)&1) != ((words>>j)&1))
        sound = not np.any(cov & ~prim); comp = not np.any(prim & ~cov)
        bad = np.nonzero(prim & ~cov)[0]
        ex = format(int(bad[0]), f'0{n}b')[::-1] if len(bad) else ''
        print(f"  lam={lam} sound={sound} complete={comp} uncovered={len(bad)} {ex}")
        if not comp: break
