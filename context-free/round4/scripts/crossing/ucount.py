import sys
from fracpos import coverage
from periodic import covered_G, soundness
print("G('mid',) soundness pieces<=11, unsound:",len(soundness(11,('mid',))))
for n in range(2,int(sys.argv[1])+1):
    tot,unc=coverage(n)
    rest=[w for w in unc if not covered_G(w,('mid',))]
    print(n,"conj classes",tot,"U_n (uncovered by all 18 classes)",len(rest),rest)
