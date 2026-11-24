/* r7_uncouple_B.c : rotation coverage of sound (non-CF) certificates.
   L_A = P ∩ {h<=0 on [0,ceil(n/2)]}   (= Lemma SA's D_b.P with |x|>=|y|, see report)
   L_B = {H>=1, h<=0 on [0,ceil(n/2)]}  (drop P)
   Ch  = {n*h(j) - j*H < 0 for 0<j<n}   (strictly below chord)
   coverage: word covered if some rotation of w or of swap(w) is in L.
   usage: ./r7B exh NMAX   |  ./r7B mc n samples seed  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MX 20010
static int L[2*MX+2]; static int n;
static int dq[2*MX+2];
/* winmax[i] = max L[i..i+len] inclusive, for i in [0,n) ; L defined on [0,2n] */
static void winmax(int len,int*out){ int hd=0,tl=0; int j=0;
  for(int i=0;i<n;i++){ while(j<=i+len){ while(tl>hd && L[dq[tl-1]]<=L[j]) tl--; dq[tl++]=j; j++; }
    while(dq[hd]<i) hd++; out[i]=L[dq[hd]]; } }
static int wmA[MX],wmP[MX];
/* returns bitmask: 1=LA,2=LB,4=Ch covered (for this orientation) */
static int cov(const char*w){ L[0]=0; for(int i=0;i<2*n;i++) L[i+1]=L[i]+(w[i%n]?1:-1);
  int H=L[n], r=0; int m=(n+1)/2;
  /* Chord: unique argmax of T over cyclic positions */
  { long best=-(1L<<60); int cnt=0; for(int i=0;i<n;i++){ long T=(long)n*L[i]-(long)i*H; if(T>best){best=T;cnt=1;} else if(T==best) cnt++; } if(cnt==1) r|=4; }
  if(H>=1){ winmax(m,wmA); winmax(n-1,wmP);
    for(int i=0;i<n;i++){ if(wmA[i]<=L[i]){ r|=2; if(wmP[i]<L[i]+H) r|=1; } } }
  return r; }
static int primitive(const char*w){ for(int d=1;d<n;d++) if(n%d==0){ int ok=1; for(int i=d;i<n;i++) if(w[i]!=w[i-d]){ok=0;break;} if(ok) return 0;} return 1; }
static unsigned long long s_=88172645463325252ULL; static unsigned long long xr(){ s_^=s_<<13; s_^=s_>>7; s_^=s_<<17; return s_; }
int main(int argc,char**argv){ char w[MX],sw[MX];
  if(!strcmp(argv[1],"exh")){ int NM=atoi(argv[2]);
    for(n=2;n<=NM;n++){ long prim=0,miss[3]={0,0,0}; unsigned N=1u<<n;
      for(unsigned x=0;x<N;x++){ for(int i=0;i<n;i++){ w[i]=(x>>i)&1; sw[i]=!w[i]; }
        if(!primitive(w)) continue; prim++; int c=cov(w)|cov(sw);
        for(int k=0;k<3;k++) if(!(c>>k&1)) miss[k]++; }
      printf("n=%2d prim=%9ld missLA=%9ld (%.4f) missLB=%9ld (%.4f) missCh=%7ld (%.5f)\n",n,prim,miss[0],(double)miss[0]/prim,miss[1],(double)miss[1]/prim,miss[2],(double)miss[2]/prim); fflush(stdout);} }
  else { n=atoi(argv[2]); int S=atoi(argv[3]); s_+=atoi(argv[4]); long miss[3]={0,0,0};
    for(int t=0;t<S;t++){ for(int i=0;i<n;i++){ w[i]=xr()>>63; sw[i]=!w[i]; } int c=cov(w)|cov(sw); for(int k=0;k<3;k++) if(!(c>>k&1)) miss[k]++; }
    printf("MC n=%d S=%d missLA=%.4f missLB=%.4f missCh=%.4f  (sqrt(n)*missCh=%.3f)\n",n,S,(double)miss[0]/S,(double)miss[1]/S,(double)miss[2]/S,(double)miss[2]/S*__builtin_sqrt(n)); }
  return 0; }
