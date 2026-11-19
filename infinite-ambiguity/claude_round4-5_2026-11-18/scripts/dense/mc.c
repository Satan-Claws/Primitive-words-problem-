/* Monte Carlo density of W for large n (same predicate as window.c). */
#include <stdio.h>
#include <stdlib.h>
int main(){ int Ns[]={100,401,1000,2001}; srand(12345);
 for(int k=0;k<4;k++){int n=Ns[k],h=n/2,T=4000,hit=0; int*S=malloc(sizeof(int)*(2*n+2)); char*c=malloc(n);
  for(int r=0;r<T;r++){ for(int t=0;t<n;t++) c[t]=rand()&1; S[0]=0; for(int t=0;t<2*n;t++) S[t+1]=S[t]+(c[t%n]?-1:1);
   int D=S[n],ok=0; for(int i=0;i<n&&!ok;i++){int g=1; for(int t=i+1;t<=i+h;t++){int x=S[t]-S[i];
     if(D>0?(x>0):D==0?(x>=0):(x<0)){g=0;break;}} if(g)ok=1;} hit+=ok;}
  printf("n=%d  W density ~ %.3f (+-%.3f)\n",n,hit/(double)T,1/ (2*__builtin_sqrt(T)));}
}
