"""r18_dwfix: exact DP of P_z(tau_W > m) for ALL starting points z, wedge W = {x<y, y>=0}
(doubled coords (x,y)=(2A,2B), steps (+-1,+-1) uniform; opening 3pi/4, apex 0).
Reports, for each m, sup_z m^{2/3} u_m(z)/(1+|z|)^{4/3} and sup_z m^{2/3} u_m(z)/h'(z),
h' = rho'^{4/3} sin(4/3 phi') w.r.t. apex shifted by 2 along the bisector (same angle).
Exactness: box half-width L; u_m(z) is exact whenever dist(z, box edge) > m (outside = 0 is a
lower bound, outside = 1 an upper bound; we run both and report the sup over z in the exact zone)."""
import numpy as np
L, MMAX, RS = 700, 512, 180          # box half-width, max steps, start radius scanned
n = 2*L+1
X, Y = np.meshgrid(np.arange(-L, L+1), np.arange(-L, L+1), indexing='ij')
inW = (X < Y) & (Y >= 0)
def step(u, pad):
    v = np.pad(u, 1, constant_values=pad)
    s = (v[2:, 2:] + v[2:, :-2] + v[:-2, 2:] + v[:-2, :-2]) / 4.0
    return np.where(inW, s, 0.0)
th0, Th, p = np.pi/4, 3*np.pi/4, 4/3
bis = th0 + Th/2
ax, ay = -2*np.cos(bis), -2*np.sin(bis)          # shifted apex a'
rho = np.hypot(X-ax, Y-ay); ang = np.arctan2(Y-ay, X-ax) - th0
hp = np.where(inW, rho**p*np.sin(p*np.clip(ang, 0, Th)), np.nan)
r = np.hypot(X, Y)
zone = inW & (r <= RS)
ulo = inW.astype(float); uhi = ulo.copy()
checks = {8, 16, 32, 64, 128, 256, 512}
print("m  sup m^(2/3)u/(1+|z|)^(4/3) [argmax]  sup m^(2/3)u/h'  u_m(0,1)*m^(2/3)  maxgap(lo,hi)")
for m in range(1, MMAX+1):
    ulo = step(ulo, 0.0); uhi = step(uhi, 1.0)
    if m in checks:
        ok = zone & (np.minimum(L-np.abs(X), L-np.abs(Y)) > m)
        a = np.where(ok, uhi*m**(2/3)/(1+r)**p, 0); i = np.unravel_index(a.argmax(), a.shape)
        b = np.where(ok, uhi*m**(2/3)/hp, 0)
        gap = np.max(np.where(ok, uhi-ulo, 0))
        print(f"{m:4d} {a.max():.4f} [{X[i]},{Y[i]}] {np.nanmax(b):.4f} {uhi[L, L+1]*m**(2/3):.4f} {gap:.1e}")
