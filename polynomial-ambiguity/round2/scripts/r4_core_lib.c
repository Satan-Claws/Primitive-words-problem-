/* r4_core_lib.c -- exact membership / tree counts for the R4-A uniform gadget library.
   word w: bit k = letter k (1 = b, 0 = a), length n <= 30.
   Gadgets (see r4_core.md for soundness proofs):
     LIN  : Parikh lines  c1*#f - c2*#h = +-1, f,h in {a,b}  (Lemma O, poly_L.md), plus #a=1, #b=1
     FOLD : fold certificates on x = b-indicator (G_fold, r3_offw.md)
     FL_K : factor-count lines on cyclic occurrence counts of factors of length <= K
     LF_K : fold certificates on the occurrence indicator x^f of each factor f, 2<=|f|<=K
     PF   : "pair-fold": fold certificates on x^f - x^h (signed features), |f|=|h|<=KP
*/
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

static int N; static uint32_t MASK;
static inline uint32_t rotr(uint32_t w, int d){ if(!d) return w; return ((w>>d)|(w<<(N-d)))&MASK; }
static int R = 3;
static int T[65][65]; /* T[o1][o2] = #{(c1,c2) in [1,R]^2, gcd=1, c1 o1 - c2 o2 = +-1} */
static int gcd(int a,int b){ while(b){int t=a%b;a=b;b=t;} return a; }
void init_table(int r){ R=r; for(int a=0;a<65;a++)for(int b=0;b<65;b++){int c=0;
  for(int c1=1;c1<=R;c1++)for(int c2=1;c2<=R;c2++){ if(gcd(c1,c2)!=1) continue; int v=c1*a-c2*b; if(v==1||v==-1) c++;} T[a][b]=c;} }

static int primitive(uint32_t w){
  for(int p=2;p<=N;p++){ if(N%p) continue; int isp=1; for(int q=2;q*q<=p;q++) if(p%q==0){isp=0;break;} if(!isp) continue;
    if(rotr(w,N/p)==w) return 0; }
  return 1;
}
/* fold certificate count for integer feature vector x[0..N-1] */
static int foldcountn(const int *x,int N){
  int cnt=0;
  for(int m=0;m<N;m++){
    int pos=0,neg=0;
    for(int i=0;i<m-i && !(pos&&neg);i++){ int d=x[m-i]-x[i]; if(d>0)pos=1; else if(d<0)neg=1; }
    for(int L=m+1,Rr=N-1;L<Rr && !(pos&&neg);L++,Rr--){ int d=x[L]-x[Rr]; if(d>0)pos=1; else if(d<0)neg=1; }
    if(pos!=neg) cnt++;
  }
  return cnt;
}
static int foldcount(const int *x){ return foldcountn(x,N); }
/* cyclic run-length sequences: alpha[i] = i-th a-run, beta[i] = following b-run; returns r (0 if unary) */
static int runs(uint32_t w,int *alpha,int *beta){
  int nb=__builtin_popcount(w); if(nb==0||nb==N) return 0;
  int s=0; while(!(((w>>s)&1)==0 && ((w>>((s+N-1)%N))&1)==1)) s++;  /* s = start of an a-run */
  int r=0,i=0;
  while(i<N){ int la=0,lb=0; while(i<N && !((w>>((s+i)%N))&1)){la++;i++;} while(i<N && ((w>>((s+i)%N))&1)){lb++;i++;}
    alpha[r]=la; beta[r]=lb; r++; }
  return r;
}
static void occvec(uint32_t w,int L,int *occ /*size 2^L*/, int *ind /* N x? optional: index per position */){
  memset(occ,0,sizeof(int)<<L);
  uint32_t m=(1u<<L)-1;
  for(int i=0;i<N;i++){ uint32_t r=rotr(w,i); uint32_t f;
    if(L<=N) f=r&m; else { f=0; for(int t=0;t<L;t++) f|=((w>>((i+t)%N))&1u)<<t; }
    occ[f]++; if(ind) ind[i]=(int)f; }
}
/* per-gadget tree counts into g[0..4] (LIN,FOLD,FL,LF,PF). lazy: if lazy, stop after first covering gadget */
void eval_word(uint32_t w,int K,int KP,int stage,int lazy,int *g){
  for(int t=0;t<8;t++) g[t]=0;
  int nb=__builtin_popcount(w), na=N-nb;
  { int c=T[na][nb]; if(na==1)c++; if(nb==1)c++; g[0]=c; }
  if(lazy&&g[0]) return;
  int x[32]; for(int i=0;i<N;i++) x[i]=(w>>i)&1;
  g[1]=foldcount(x); if(lazy&&g[1]) return;
  if(stage>=1){ int nf=0; int all[1<<7];
    for(int L=1;L<=K;L++){ int o[1<<6]; occvec(w,L,o,0); for(int f=0;f<(1<<L);f++) all[nf++]=o[f]; }
    int c=0;
    for(int i=2;i<nf;i++) if(all[i]==1) c++;
    for(int i=0;i<nf;i++)for(int j=i+1;j<nf;j++){ if(j<2) continue; c+=T[all[i]][all[j]]; }
    g[2]=c; if(lazy&&c) return; }
  if(stage>=2){ int c=0; int ind[32];
    for(int L=2;L<=K;L++){ int o[1<<6]; occvec(w,L,o,ind);
      for(int f=0;f<(1<<L);f++){ if(o[f]==0) continue; int y[32]; for(int i=0;i<N;i++) y[i]=(ind[i]==f); c+=foldcount(y); if(lazy&&c){g[3]=c;return;}} }
    g[3]=c; }
  if(stage>=3){ int c=0; int ind[32];
    for(int L=2;L<=KP;L++){ int o[1<<6]; occvec(w,L,o,ind);
      for(int f=0;f<(1<<L);f++)for(int h=f+1;h<(1<<L);h++){ if(!o[f]&&!o[h]) continue;
        int y[32]; for(int i=0;i<N;i++) y[i]=(ind[i]==f)-(ind[i]==h); c+=foldcount(y); if(lazy&&c){g[4]=c;return;}} }
    g[4]=c; if(lazy&&c) return; }
  if(stage>=4){ int al[32],be[32]; int r=runs(w,al,be); int c=0;
    if(r>=2){ c=foldcountn(al,r)+foldcountn(be,r); }
    g[5]=c; if(lazy&&c) return; }
}
static uint32_t rev(uint32_t w){ uint32_t r=0; for(int i=0;i<N;i++) if((w>>i)&1) r|=1u<<(N-1-i); return r; }
uint32_t canon(uint32_t w){
  uint32_t best=0xffffffffu; uint32_t vs[4]={w,rev(w),(~w)&MASK,(~rev(w))&MASK};
  for(int t=0;t<4;t++) for(int i=0;i<N;i++){ uint32_t r=rotr(vs[t],i); if(r<best) best=r; }
  return best;
}
/* full sweep. counts[0]=|Q_n|; counts[1+s]=#covered by gadgets 0..gs(s) cumulative (s=0: LIN+FOLD, 1:+FL, 2:+LF, 3:+PF)
   full=1 -> evaluate all gadgets on all words (for max ambiguity, maxamb[s] = max sum of tree counts of stage-s library) */
static int gs_of(int s){ return s==0?2:(s+2); }
long sweep(int n,int K,int KP,int stage,int full,long *counts,int *maxamb,uint32_t *unc,long cap){
  N=n; MASK=((1u<<n)-1);
  long nu=0; memset(counts,0,sizeof(long)*8); for(int s=0;s<8;s++) maxamb[s]=0;
  for(uint32_t w=0; w<=MASK; w++){
    if(primitive(w)){
      counts[0]++;
      int g[8]; eval_word(w,K,KP,stage,!full,g);
      int covered=0; int a=0;
      for(int s=0;s<=stage;s++){
        int lo=(s==0)?0:gs_of(s-1), hi=gs_of(s);
        for(int t=lo;t<hi;t++){ a+=g[t]; if(g[t]) covered=1; }
        if(covered) counts[1+s]++;
        if(a>maxamb[s]) maxamb[s]=a;
      }
      if(!covered){ if(nu<cap) unc[nu]=w; nu++; }
    }
    if(w==MASK) break;
  }
  return nu;
}
void setn(int n){ N=n; MASK=(1u<<n)-1; }
void eval1(uint32_t w,int n,int K,int KP,int stage,int *g){ setn(n); eval_word(w,K,KP,stage,0,g); }
