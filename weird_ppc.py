import time


class Sudoku:
    def __init__(self, fields):
        if isinstance(fields, Sudoku):
            other = fields
            copy = lambda x: x.copy()
            self.fields = other.fields.copy()
            self.planes = list(map(copy, other.planes))
            self.lines = list(map(copy, other.lines))
        else:
            self.fields = fields
            self.planes = [charset.copy() for _ in range(36)]
            self.lines = [charset.copy() for _ in range(36)]

            for i, field in enumerate(fields):
                self.planes[i] -= set(field)
                for j, c in enumerate(field):
                    self.lines[j].discard(c)

    # def solve(self, progress=0., weight=1., depth=1):
    def solve(self):
        # print(f'\r{progress:7.7} {depth}', end='')
        if not any(c == '*' for field in self.fields for c in field):
            print('\r'+self.fields[0])
            return self.fields[0]
        i, j = min(
            ([i, j] for i, field in enumerate(self.fields) for j, c in enumerate(field) if c == '*'),
            key=lambda ij: len(self.planes[ij[0]] & self.lines[ij[1]])
        )
        for char in self.planes[i] & self.lines[j]:
            new = Sudoku(self)
            new.set(i, j, char)
            new.optimize()
            # res = new.solve(progress + i * weight / len(chars), weight / len(chars), depth + 1)
            res = new.solve()
            # if res is not None:
            #     return res

    def optimize(self):
        while True:
            found = False
            for i, field in enumerate(self.fields):
                for j, c in enumerate(field):
                    if c == '*':
                        chars = self.planes[i] & self.lines[j]
                        if len(chars) == 1:
                            found = True
                            self.set(i, j, list(chars)[0])
            if not found:
                break

    def set(self, i, j, c):
        s = list(self.fields[i])
        s[j] = c
        self.fields[i] = ''.join(s)
        self.planes[i].discard(c)
        self.lines[j].discard(c)

    def valid(self):
        for field in self.fields:
            if len(field) != len(set(field)):
                return False
        for j in range(36):
            if len({field[j] for field in self.fields}) != 36:
                return False
        return True


sudoku = """
mctf{************5vhnj6*iped2q3**4wb
c**hij0_ozk*abq**2*}ymt*g*5x1{s3r*4e
b**i*614*fjzwny*d*utora{**q}e_v*s3cl
_*koq*mdnv**lfa*2*i*j3ezwh**65**u1p*
5*1nrh*x_3pwf*mvaobj2gc*t}{*l*u6**qk
4*iwbkh3g*fnqj0*zuox_avl6ctemd5{**}p
oef4n_y}d*6jm3trwi0guk1bqxvahczlp{5s
3*2skwo5mb4u*hja0dz1it*}_g*lfy6n{*vc
6r5dl4x{zn*givehcqjb3_m*at*2}swuyof*
*{yahr306co2_qlus***gv4dji1zkpx*t}*w
goz*3mar}*qd*ixlnhtw4ebsu1*c02y**p*v
ydxjgznfu*v1*c_m*3ks*0iap{**46e2**hq
l36*xb*kt{yrs_gz*mf*}w*ch*2n**p4**j0
e6r3dy**a*z*54*1bcxohswtm2_gnf0vljiu
**_gvp6zldxo**n{tk*5cu}*efsma0qw4i*h
vag*ynrqs**3utdi_*5epc2xbjl*{1hmok6}
stw*a}dcr5n{h2u**43v*p*qyoz*gmkieb06
ui*q2dglyo*a1ph4fen*z}xkc5*6**tsv_{3
{zuvs5**p*ry0k*}*xem1bqh*ni*c3jdagt*
*p3cwib14*d_*5zk*{ra6hng*lyuqe2*fvot
2vjl*xs6ig***1}*uta*m*_*z3*bp**c***5
kjc_putw****}*s*{l**qf*0**3voa*enmxr
r1lbf{**vq*mt65x3pgi*4o_**chdka*wu*y
qu4t}35***ac*{ophj*2xig*0e61znf*b**m
wgdp41*hq*{evaiy*n*l5zj6*_x3buc*m0s2
*lvzco4mbj*}{*p6*fh*td0i5y*_xw1q32kg
*q*e6vwb3p}l*xf*5r{_k2h**maistg1cyuz
05*x1lui*e34zsvnya2*w{*jr*fk_*dbgtm*
hma6_eq*k*csxwb*v}1p{yzfd0o53g4r**2i
*_qmzf*s5*uhg}cbe6**aly1240{*vnodx3j
pn*k*c}e*6i*bg{*q0_yv1l23u*twjo*hzrd
z2{}*sfy**lt*m63j1p4bokwnqr*vx*hicga
xk*ye2cjf0gi*z3q*vlus*{5odhr*bm_1wan
fwouj*it*h564l2cks***n3mv*}*yz*x0a*_
1}p*u0*o{a*f3yreiw**dxsnkvmq5hlg_6b4
i0*rtqzajm1p*ow2g_s3*5dv{bn4*l}*6**x
"""
sudoku = [field.strip() for field in sudoku.split('\n') if field.strip() != ""]
charset = set(''.join(sudoku))
charset.discard('*')

t = time.time()
Sudoku(sudoku).solve()
print(time.time() - t)