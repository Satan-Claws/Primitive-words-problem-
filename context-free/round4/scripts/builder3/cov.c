/* builder3: coverage of CF certificate families on primitive necklaces. a=0,b=1. One core.
   usage: cov MODE N0 N1 [B]   MODE: cov (coverage table + miss dump), sound (all words n<=N1 non-primitive rejected)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 512
static int B = 3; static int ANYT=0;
static int gcd(int a,int b){ if(a<0)a=-a; if(b<0)b=-b; while(b){int t=a%b;a=b;b=t;} return a; }

/* ---- D: builder Theorem D: some rotation v with dom(v) or dom(v[1:]) ---- */
static int domv(const int*v,int m){ int st=0; for(int i=0;i<m/2;i++){ if(v[i]>v[m-1-i])return 0; if(v[i]<v[m-1-i])st=1;} return st; }
static int cert_D(const int*w,int n){ int v[2*MAXN]; for(int r=0;r<n;r++){ for(int i=0;i<n;i++)v[i]=w[(i+r)%n]; if(domv(v,n)||domv(v+1,n-1))return 1;} return 0; }

/* ---- GB: letter fold counts m_c, r_c ---- */
static int cert_GB(const int*w,int n){ for(int c=0;c<n;c++){ int m=0; for(int i=0;i<n;i++) if(w[i]==1&&w[((c-i)%n+n)%n]==0)m++; int r=n-2*m; if((m<=B||r<=B)&&gcd(m,r)==1)return 1;} return 0; }

/* ---- run cycle ---- */
static int runs(const int*w,int n,int*L){ int st=-1; for(int i=0;i<n;i++) if(w[i]!=w[(i-1+n)%n]){st=i;break;} if(st<0)return 0;
  int K=0,i=0; while(i<n){ int j=i; while(j<n&&w[(st+j)%n]==w[(st+i)%n])j++; L[K++]=j-i; i=j;} return K; }
static int cert_RD(const int*w,int n){ int L[MAXN]; int K=runs(w,n,L); if(!K)return 0;
  for(int c=0;c<K;c+=2) for(int sg=1;sg>=-1;sg-=2){ int st=0,ok=1; for(int t=1;t<K/2;t++){ int i=(c/2+t)%K; int x=L[i],y=L[((c-i)%K+K)%K]; if(sg<0){int z=x;x=y;y=z;} if(x>y){ok=0;break;} if(x<y)st=1;} if(ok&&st)return 1;} return 0; }
static int cert_RGB(const int*w,int n){ int L[MAXN]; int K=runs(w,n,L); if(!K)return 0;
  for(int c=0;c<K;c+=2){ int nz=0; for(int i=0;i<K;i++) if(L[i]!=L[((c-i)%K+K)%K])nz++; int mm=nz/2,r=K-2*mm; if(mm>=1&&(mm<=B||r<=B)&&gcd(mm,r)==1)return 1;} return 0; }

/* ---- E': |w|_b-|w|_a = +-1 ---- */
static int cert_EP(const int*w,int n){ int b=0; for(int i=0;i<n;i++)b+=w[i]; int d=2*b-n; return d==1||d==-1; }
/* ---- PAR: Parikh lines alpha*A-beta*Bc=+-1 (alpha,beta<=B) or min(A,Bc)<=B with gcd 1 (regular/one-counter) ---- */
static int cert_PAR(const int*w,int n){ int b=0; for(int i=0;i<n;i++)b+=w[i]; int a=n-b; if(gcd(a,b)!=1)return 0; if(a<=B||b<=B)return 1;
  for(int al=1;al<=B;al++)for(int be=1;be<=B;be++){ int d=al*a-be*b; if(d==1||d==-1)return 1;} return 0; }

/* ---- block vector: blocks = a-runs before each b (letter 'one' plays b). returns K = #ones ---- */
static int blocks(const int*w,int n,int one,int*x){ int K=0,st=-1; for(int i=0;i<n;i++) if(w[i]==one){st=i;break;} if(st<0)return 0;
  int cnt=0; for(int j=1;j<=n;j++){ int c=w[(st+j)%n]; if(c==one){x[K++]=cnt;cnt=0;} else cnt++; } return K; }
/* generalized L_l*: reflection R(i)=s-i on Z_K (any s), l|K, K>=2l; some R-fixed class f with D|_f = e_j - e_{Rj} (j!=Rj),
   other fixed classes D==0, swapped classes single-signed. */
static int Cl_any(const int*x,int K,int l){ if(K%l||K<2*l)return 0; int D[MAXN];
  for(int s=0;s<K;s++){ for(int i=0;i<K;i++)D[i]=x[i]-x[((s-i)%K+K)%K];
    int ok=1, fcand=-1, jfound=-1;
    for(int c=0;c<l&&ok;c++){ int cr=((s-c)%l+l)%l;
      if(cr==c){ /* fixed class: either all zero or exactly one +1 and one -1 */
        int np=0,nn=0,nz=0,jp=-1; for(int i=c;i<K;i+=l){ if(D[i]==0)nz++; else if(D[i]==1||(ANYT&&D[i]>0)){np++;jp=i;} else if(D[i]==-1||(ANYT&&D[i]<0))nn++; else {ok=0;break;} }
        if(!ok)break; if(np==0&&nn==0)continue; if(np==1&&nn==1&&fcand<0){fcand=c;jfound=jp;} else ok=0;
      } else if(c<cr){ int pos=0,neg=0; for(int i=c;i<K;i+=l){ if(D[i]>0)pos=1; if(D[i]<0)neg=1;} if(pos&&neg)ok=0; }
    }
    if(ok&&fcand>=0)return 1; }
  return 0; }
static int LMAX=6;
static int cert_L(const int*w,int n){ int x[MAXN]; for(int one=0;one<2;one++){ int K=blocks(w,n,one,x); if(K<1)continue; for(int l=1;l<=LMAX;l++) if(Cl_any(x,K,l))return 1;} return 0; }
/* ---- BGB: block-level Lemma O, class {D>0} size mm with mm<=B or K-2mm<=B, gcd(mm,K)=1... use gcd(mm,K-2mm)=1 ---- */
static int cert_BGB(const int*w,int n){ int x[MAXN]; for(int one=0;one<2;one++){ int K=blocks(w,n,one,x); if(K<2)continue;
  for(int s=0;s<K;s++){ int mm=0; for(int i=0;i<K;i++) if(x[i]>x[((s-i)%K+K)%K])mm++; int r=K-2*mm; if(mm>=1&&(mm<=B||r<=B)&&gcd(mm,r)==1)return 1; } } return 0; }


/* ---- walk.md T-operator: first-passage pieces (a=+1,b=-1). level0 = E' (|Delta|=1) or (useG) G-weights ---- */
static int pieces(const int*w,int n,int*typ,int*first){ /* returns D>=1 after swap if needed; typ[j]=0 if piece=='a', 1 if starts 'ba', 2 if starts 'bb' */
  int D=0; for(int i=0;i<n;i++)D+=w[i]?-1:1; int sw=0; if(D==0)return 0; if(D<0){sw=1;D=-D;}
  int S=0,best=0,ts=0; for(int t=1;t<n;t++){ S+=((w[t-1]^sw)?-1:1); if(S>best){best=S;ts=t;} }
  int lev=0,cur=0,len=0,f0=-1,f1=-1; int np=0;
  for(int j=0;j<n;j++){ int c=w[(ts+j)%n]^sw; if(len==0)f0=c; else if(len==1)f1=c; len++; cur+=c?-1:1;
    if(cur>lev){ lev=cur; typ[np++]= (len==1)?0:(f1==0?1:2); len=0; } }
  (void)first; return np; }
static int inG(const int*w,int n){ int typ[MAXN]; int D=pieces(w,n,typ,0); if(!D)return 0; int g=0; for(int j=0;j<D;j++) g+= typ[j]==0?1:(typ[j]==1?-2:0); return g==1||g==-1; }
static int inT(const int*w,int n,int k,int useG){
  if(useG&&inG(w,n))return 1;
  if(k==0) return cert_EP(w,n);
  int typ[MAXN]; int D=pieces(w,n,typ,0); if(!D)return 0; int v[MAXN]; for(int j=0;j<D;j++)v[j]=typ[j]?1:0; return inT(v,D,k-1,useG); }
static int cert_T1(const int*w,int n){ return inT(w,n,1,0); }
static int cert_T2(const int*w,int n){ return inT(w,n,2,0); }
static int cert_T3(const int*w,int n){ return inT(w,n,3,0); }
static int cert_TG2(const int*w,int n){ return inT(w,n,2,1); }

static int cert_BASE(const int*w,int n){ return cert_D(w,n)||cert_GB(w,n)||cert_RD(w,n)||cert_RGB(w,n)||cert_EP(w,n)||cert_PAR(w,n)||cert_L(w,n)||cert_BGB(w,n)||inG(w,n); }
static int TAK=2;
static int inTA(const int*w,int n,int k){ if(n<=0)return 0; if(cert_BASE(w,n))return 1; if(k==0)return 0;
  int typ[MAXN]; int D=pieces(w,n,typ,0); if(!D||D==n)return 0; int v[MAXN]; for(int j=0;j<D;j++)v[j]=typ[j]?1:0; return inTA(v,D,k-1); }
static int cert_TA(const int*w,int n){ return inTA(w,n,TAK); }
typedef int (*cf)(const int*,int);
#define NC 13
static const char*NAMES[NC]={"D","GB","RD","RGB","EP","PAR","L","BGB","T1","T2","T3","TG2","TA"};
static cf CERTS[NC]={cert_D,cert_GB,cert_RD,cert_RGB,cert_EP,cert_PAR,cert_L,cert_BGB,cert_T1,cert_T2,cert_T3,cert_TG2,cert_TA};

static int isprim(const int*w,int n){ for(int d=1;d<n;d++) if(n%d==0){ int ok=1; for(int i=d;i<n;i++) if(w[i]!=w[i-d]){ok=0;break;} if(ok)return 0;} return 1; }

static int n_glob; static long missTA; static long tot, miss[NC], missU0, missU, missUT;
static FILE*dump;
static void visit(const int*w,int n){ /* w Lyndon */
  tot++; int r[NC]; for(int k=0;k<NC;k++){ r[k]=CERTS[k](w,n); if(!r[k])miss[k]++; }
  int u0=r[0]||r[1]||r[2]||r[3]; if(!u0)missU0++;
  int ut=u0||r[8]||r[9]||r[10]||r[11]; if(!ut)missUT++; int u=ut||r[4]||r[5]||r[6]||r[7]; if(!r[12])missTA++; if(!u)missU++; if(!u&&!r[12]){ if(dump){ for(int i=0;i<n;i++)fputc("ab"[w[i]],dump); fputc('\n',dump);} }
}
static int a[MAXN+1];
static void lyn(int n){ /* FKM iterative */
  int w[MAXN+1]; int i; for(i=0;i<=n;i++)w[i]=0; int len=1; w[1]=0; /* use standard algorithm on 1-indexed */
  /* simple Duval generation */
  int m; int buf[MAXN]; int L=0; buf[0]=-1; L=1;
  while(L>0){ buf[L-1]++; m=L; if(m==n){ visit(buf,n);} while(L<n){ buf[L]=buf[L-m]; L++; } while(L>0&&buf[L-1]==1)L--; }
  (void)i;(void)len;(void)w;
}
int main(int argc,char**argv){ const char*mode=argv[1]; int N0=atoi(argv[2]),N1=atoi(argv[3]); if(argc>4)B=atoi(argv[4]); if(argc>5)LMAX=atoi(argv[5]); if(argc>6)ANYT=atoi(argv[6]); if(argc>8)TAK=atoi(argv[8]);
  if(!strcmp(mode,"mc")){ int S=atoi(argv[7]); srand(12345); static int w[MAXN]; for(int n=N0;n<=N1;n=(n<40?n+6:(n<100?n+20:n*2+1))){ long hit[NC]={0}; long u0=0,u=0,ut=0,prim=0;
      for(int t=0;t<S;t++){ for(int i=0;i<n;i++)w[i]=(rand()>>7)&1; if(!isprim(w,n))continue; prim++; int r[NC]; for(int k=0;k<NC;k++){r[k]=CERTS[k](w,n); hit[k]+=r[k];}
        int a0=r[0]||r[1]||r[2]||r[3]; u0+=a0; int at=a0||r[8]||r[9]||r[10]||r[11]; ut+=at; u+= at||r[4]||r[5]||r[6]||r[7]; }
      printf("n=%d S=%ld",n,prim); for(int k=0;k<NC;k++)printf(" %s:%.3f",NAMES[k],(double)hit[k]/prim); printf(" | CFU(b2):%.3f CFU+T:%.3f ALL:%.3f\n",(double)u0/prim,(double)ut/prim,(double)u/prim); fflush(stdout);} return 0; }
  if(!strcmp(mode,"sound")){ int w[MAXN]; for(int n=1;n<=N1;n++){ long bad=0; for(long x=0;x<(1L<<n);x++){ for(int i=0;i<n;i++)w[i]=(x>>i)&1; if(isprim(w,n))continue; for(int k=0;k<NC;k++) if(CERTS[k](w,n)){ bad++; fprintf(stderr,"UNSOUND %s n=%d x=%lx\n",NAMES[k],n,x);} } printf("n=%d unsound=%ld\n",n,bad); fflush(stdout);} return 0; }
  for(int n=N0;n<=N1;n++){ tot=0; memset(miss,0,sizeof miss); missU0=missU=missUT=missTA=0; char fn[64]; sprintf(fn,"miss_%d.txt",n); dump=fopen(fn,"w"); lyn(n); fclose(dump);
    printf("n=%d nk=%ld",n,tot); for(int k=0;k<NC;k++)printf(" %s:%ld",NAMES[k],miss[k]); printf(" | CFU(b2):%ld CFU+T:%ld ALL:%ld TAmiss:%ld\n",missU0,missUT,missU,missTA); fflush(stdout); }
}
