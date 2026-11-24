/* r7_uncouple_A.c : uncoupled split languages X.Y, exhaustive n<=NMAX.
   bit i of w = letter i (1=a,0=b). h = #a-#b prefix walk.
   Variants of X (zero s of h, prefix condition on [0,s]):
     X0: b-first Dyck  (h<=0 on [0,s])   X1: a-first Dyck (h>=0)   X2: any balanced (h(s)=0)
     X3: b-first Dyck nonempty (s>0)
   Variants of Y (nonempty, on [s,n)): Y0 strict: h(j)<H for s<=j<n ; Y1 weak: h(j)<=H, and H>=1.
   For each variant: count members, nonprimitive members, max #splits (= ambiguity of X.Y with X,Y unambiguous),
   and test conjecture C: nonprim member w=u^p  <=>  u (primitive root) is itself a member;
   also test V0 == P (=every suffix a-heavy). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n; static int h[64];
static int root(unsigned w){ for(int d=1; d<n; d++) if(n%d==0){ unsigned m=(1u<<d)-1, u=w&m; int ok=1; for(int i=d;i<n;i+=d) if(((w>>i)&m)!=u){ok=0;break;} if(ok) return d;} return n; }
static int splits(unsigned w,int len,int xv,int yv){
  int hh[64]; hh[0]=0; for(int i=0;i<len;i++) hh[i+1]=hh[i]+(((w>>i)&1)?1:-1);
  int H=hh[len], cnt=0; if(H<1) return 0;
  int ok=1; /* prefix condition */
  for(int s=0;s<len;s++){ /* y nonempty: s<len */
    if(xv==0 && hh[s]>0) ok=0; if(xv==1 && hh[s]<0) ok=0;
    if(!ok) break;
    if(hh[s]!=0) continue; if(xv==3 && s==0) continue;
    int good=1; for(int j=s;j<len;j++){ if(yv==0? hh[j]>=H : hh[j]>H){good=0;break;} }
    cnt+=good; }
  return cnt; }
int main(int argc,char**argv){ int NMAX=atoi(argv[1]);
  for(n=2;n<=NMAX;n++){ unsigned N=1u<<n;
    for(int xv=0;xv<4;xv++) for(int yv=0;yv<2;yv++){
      long mem=0,np=0,viol=0,notP=0; int maxs=0; int shown=0;
      long conv=0; for(unsigned w=0;w<N;w++){ int c=splits(w,n,xv,yv); if(!c){ int d=root(w); if(d<n && splits(w&((1u<<d)-1),d,xv,yv)) conv++; continue;} mem++; if(c>maxs) maxs=c;
        if(xv==0&&yv==0){ /* P test */ int hh=0,H=0; for(int i=0;i<n;i++) H+=((w>>i)&1)?1:-1; int suf=0,isP=1; for(int i=n-1;i>=0;i--){suf+=((w>>i)&1)?1:-1; if(suf<=0){isP=0;break;}} if(!isP) notP++; (void)hh;}
        int d=root(w); if(d<n){ np++; unsigned u=w&((1u<<d)-1); int cu=splits(u,d,xv,yv); if(!cu){ viol++; if(shown<2 && n<=12){ fprintf(stderr,"n=%d X%dY%d counterex w=",n,xv,yv); for(int i=0;i<n;i++) fputc(((w>>i)&1)?'a':'b',stderr); fputc('\n',stderr); shown++; } } } }
      if(n==NMAX || n==16) printf("n=%d X%d Y%d: members=%ld nonprim=%ld maxsplits=%d rootNotMember=%ld memberRootPowerNot=%ld notP=%ld\n",n,xv,yv,mem,np,maxs,viol,conv,notP);
      }
  }
  return 0; }
