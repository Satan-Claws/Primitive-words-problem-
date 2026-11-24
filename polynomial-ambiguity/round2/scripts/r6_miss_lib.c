/* r6_miss_lib.c -- R6 fold-certificate miss set.  x[i] = 1 iff letter i is 'a'.
   For a cyclic integer feature y (y = x^phi, phi a window function) and rotation r:
     d_k^{(r)} = sum y[r..r+k) - sum y[r+n-k..r+n)          (prefix vs suffix of the rotated word)
   Tiers (bit = 1 means CERTIFIED primitive by that tier):
     bit0 A  : F_K on w            (K = [ceil(n/3), floor(n/2)], feature a)
     bit1 B  : F_max on w          (for every prime p|n, the p-block a-count vector is NOT a palindrome)
     bit2 C  : Rot(F_K)            (some rotation in F_K)
     bit3 C' : Rot(F_K) over features {a, aa, ab}
     bit4 D  : Rot(F_max)          (some rotation in F_max)
     bit5 E  : Rot(F_max) over features {a, aa, ab}
     bit6 F1 : F_0.1 on w          (as r5: [ceil(.4n), n/2] + floor(p/2)n/p for primes p<=12, p|n)
     bit7 F2 : Rot(F_0.1)
     bit8 W  : F_W on w, W = residue-dependent window (see r6_miss.md sec 3): n%6==0: [n/3,n/2];
               n even,3!|n: [2n/5,n/2]; n odd,3|n: [n/3,3n/7]; gcd(n,6)=1: [2n/5,6n/13]
               (all windows closed, integer k with lo<=k<=hi, lo=ceil, hi=floor)
     bit9 RW : Rot(F_W)
   Soundness of every tier: r6_miss.md Lemma M (block-palindrome lemma); checked exhaustively by r6_miss_exh.py.
*/
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

static int isprime(int p){ if(p<2) return 0; for(int q=2;q*q<=p;q++) if(p%q==0) return 0; return 1; }

/* S has length 2n+1, prefix sums of y doubled */
static void psum(const int *y,int n,int *S){ S[0]=0; for(int i=0;i<2*n;i++) S[i+1]=S[i]+y[i%n]; }

static int fk_at(const int *S,int n,int r,int lo,int hi){
  for(int k=lo;k<=hi;k++){ int d=(S[r+k]-S[r])-(S[r+n]-S[r+n-k]); if(d==0) return 0; }
  return 1;
}
static int fpts_at(const int *S,int n,int r,const int *pts,int np){
  for(int t=0;t<np;t++){ int k=pts[t]; int d=(S[r+k]-S[r])-(S[r+n]-S[r+n-k]); if(d==0) return 0; }
  return 1;
}
/* F_max at rotation r: certified iff for all primes p|n the block vector is not palindromic */
static int fmax_at(const int *S,int n,int r,const int *pr,int npr){
  for(int t=0;t<npr;t++){ int p=pr[t], m=n/p, pal=1;
    for(int i=0;i<p/2 && pal;i++){ int ci=S[r+(i+1)*m]-S[r+i*m]; int cj=S[r+(p-i)*m]-S[r+(p-1-i)*m]; if(ci!=cj) pal=0; }
    if(pal) return 0; }
  return 1;
}
static void window_W(int n,int *lo,int *hi){
  int a2=(n%2==0), a3=(n%3==0);
  int ln,ld,hn,hd;
  if(a2&&a3){ln=1;ld=3;hn=1;hd=2;} else if(a2){ln=2;ld=5;hn=1;hd=2;} else if(a3){ln=1;ld=3;hn=3;hd=7;} else {ln=2;ld=5;hn=6;hd=13;}
  *lo=(ln*n+ld-1)/ld; *hi=(hn*n)/hd; if(*lo<1)*lo=1;
}

/* returns tier mask; x length n (n <= 20000) */
int eval_tiers(const unsigned char *x,int n){
  static __thread int y[3][20000]; static __thread int S[3][40001];
  int pr[32],npr=0; for(int p=2;p<=n;p++) if(n%p==0&&isprime(p)) pr[npr++]=p;
  int pts[16],np=0; for(int t=0;t<npr;t++) if(pr[t]<=12) pts[np++]=(pr[t]/2)*(n/pr[t]);
  int lo=(n+2)/3, hi=n/2;
  int dlo=(int)((0.4*n)+0.999999999); if(dlo<1)dlo=1; /* ceil(.4n) */
  { /* exact ceil(2n/5) */ dlo=(2*n+4)/5; }
  int wlo,whi; window_W(n,&wlo,&whi);
  for(int i=0;i<n;i++){ int a=x[i], b=x[(i+1)%n]; y[0][i]=a; y[1][i]=a&b; y[2][i]=a&(!b); }
  for(int f=0;f<3;f++) psum(y[f],n,S[f]);
  int mask=0;
  if(fk_at(S[0],n,0,lo,hi)) mask|=1;
  if(fmax_at(S[0],n,0,pr,npr)) mask|=2;
  if(fk_at(S[0],n,0,dlo,hi)&&fpts_at(S[0],n,0,pts,np)) mask|=64;
  if(fk_at(S[0],n,0,wlo,whi)) mask|=256;
  for(int r=0;r<n;r++) if(fk_at(S[0],n,r,lo,hi)){ mask|=4; break; }
  if(mask&4) mask|=8; else { for(int f=1;f<3 && !(mask&8);f++) for(int r=0;r<n;r++) if(fk_at(S[f],n,r,lo,hi)){ mask|=8; break; } }
  for(int r=0;r<n;r++) if(fmax_at(S[0],n,r,pr,npr)){ mask|=16; break; }
  if(mask&16) mask|=32; else { for(int f=1;f<3 && !(mask&32);f++) for(int r=0;r<n;r++) if(fmax_at(S[f],n,r,pr,npr)){ mask|=32; break; } }
  for(int r=0;r<n;r++) if(fk_at(S[0],n,r,dlo,hi)&&fpts_at(S[0],n,r,pts,np)){ mask|=128; break; }
  for(int r=0;r<n;r++) if(fk_at(S[0],n,r,wlo,whi)){ mask|=512; break; }
  return mask;
}

static int primitive_w(uint32_t w,int n){
  uint32_t M=(n==32)?0xffffffffu:((1u<<n)-1);
  for(int p=2;p<=n;p++){ if(n%p||!isprime(p)) continue; int d=n/p;
    uint32_t r=((w>>d)|(w<<(n-d)))&M; if(r==w) return 0; }
  return 1;
}
/* exhaustive sweep over w in [w0,w1): counts[mask]++ for primitive words (mask has 10 bits -> 1024 bins);
   dump words with (mask & dumpbit)==0 into buf (up to cap). counts[1024] = #primitive. returns #dumped */
long sweep_range(int n,uint32_t w0,uint32_t w1,long *counts,int dumpbit,uint32_t *buf,long cap){
  unsigned char x[32]; long nd=0;
  for(uint32_t w=w0; w<w1; w++){
    if(!primitive_w(w,n)) continue;
    counts[1024]++;
    for(int i=0;i<n;i++) x[i]=(w>>i)&1;
    int m=eval_tiers(x,n); counts[m]++;
    if(!(m&dumpbit)){ if(nd<cap) buf[nd]=w; nd++; }
  }
  return nd;
}

/* batch: X is S rows of n bytes; out[s] = tier mask | (argmax-multiplicity>=2)<<10 | (argmin-multiplicity>=2)<<11 */
void eval_batch(const unsigned char *X,int S,int n,int *out){
  for(int s=0;s<S;s++){ const unsigned char *x=X+(long)s*n;
    int m=eval_tiers(x,n);
    long A=0; for(int i=0;i<n;i++) A+=x[i];
    long Sm=0, mx=-(1L<<60), mn=(1L<<60); int cx=0,cn=0;
    for(int i=0;i<n;i++){ long T=(long)n*Sm-(long)i*A; if(T>mx){mx=T;cx=1;} else if(T==mx) cx++; if(T<mn){mn=T;cn=1;} else if(T==mn) cn++; Sm+=x[i]; }
    out[s]=m|((cx>=2)<<10)|((cn>=2)<<11); }
}
