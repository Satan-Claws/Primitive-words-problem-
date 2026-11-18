/* Window certificate W (non-CF candidate, positive density) vs E'.
   W+: D>=1 and exists i with S_t <= S_i for t in (i, i+floor(n/2)]
   W0: D==0 and exists i with S_t <  S_i for t in (i, i+floor(n/2)]
   W-: mirror (D<=-1, S_t >= S_i).  Cyclic walk S_{t+n}=S_t+D.  a=+1.
   Checks soundness (all W words primitive) and prints |W_n|/2^n, |E'_n|/2^n. */
#include <stdio.h>
#include <stdlib.h>
static int prim(unsigned w,int n){ for(int d=1;d<n;d++) if(n%d==0){unsigned m=(1u<<n)-1; unsigned r=((w>>d)|(w<<(n-d)))&m; if(r==w) return 0;} return 1;}
int main(int argc,char**argv){int N=atoi(argv[1]);
 for(int n=2;n<=N;n++){ long cW=0,cE=0,bad=0; int S[200]; int h=n/2;
  for(unsigned w=0;w<(1u<<n);w++){ S[0]=0; for(int t=0;t<2*n;t++){int c=(w>>(t%n))&1; S[t+1]=S[t]+(c?-1:1);} /* bit1=b */
   int D=S[n]; if(D==-1) cE++;
   int ok=0;
   for(int i=0;i<n&&!ok;i++){ int good=1; for(int t=i+1;t<=i+h;t++){ int x=S[t]-S[i];
       if(D>0){ if(x>0){good=0;break;} } else if(D==0){ if(x>=0){good=0;break;} } else { if(x<0){good=0;break;} } }
     if(good) ok=1; }
   if(ok){cW++; if(!prim(w,n)) bad++;}
  }
  printf("n=%2d  W=%ld (%.4f)  E'=%ld (%.4f)  E'*sqrt(n)=%.3f  nonprim_in_W=%ld\n",n,cW,cW/(double)(1u<<n),cE,cE/(double)(1u<<n),cE/(double)(1u<<n)*__builtin_sqrt(n),bad);
  fflush(stdout);}
}
