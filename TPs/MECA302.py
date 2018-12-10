################################################################################
# MECA302
################################################################################


import numpy as np
import pandas as pd
from string import Template

_torseur_latex = Template(r"""$$$$ 
\begin{Bmatrix}
$rx & $mx \\
$ry & $my \\
$rz & $mz 
\end{Bmatrix}_{ ( $px , $py , $pz) , 0 }$$$$
""")


class Torseur:
    """
    Une classe de torseurs.
    
    Arguments:
    * r: la résultante
    * m: le moment
    * p: le point auquel le moment esr défini.
    """
    def __init__(self, r = [0., 0., 0.], m = [0., 0., 0.], p = [0., 0., 0.]):
        self.r = np.array(r)
        self.m = np.array(m)
        self.p = np.array(p)
    
    def transport(self, p):
        """
        Transporte le torseur en autre point p et renvoie le torseur obtenu.
        """
        p = np.array(p)
        m = self.m + np.cross((self.p-p), self.r)
        return Torseur(self.r, m, p)
        
    def __repr__(self):
        return "<Torseur: R={0}, M={1}, P={2}>".format(self.r, self.m, self.p)
    
    
    def _repr_latex_(self):
        out = {"rx": self.r[0],
               "ry": self.r[1],
               "rz": self.r[2],
               "mx": self.m[0],
               "my": self.m[1],
               "mz": self.m[2],
               "px": self.p[0],
               "py": self.p[1],
               "pz": self.p[2],
                }
        return _torseur_latex.substitute(**out )
    
    def __add__(self, T):
      sr = self.r
      sm = self.m
      T = T.transport(self.p)
      tr = T.r
      tm = T.m
      return Torseur(r = sr + tr, m = sm + tm, p = self.p)
    
    def __neg__(self):
      return Torseur(r = -self.r, m = -self.m, p = self.p)
    
    def __sub__(self, T):
      return self - T
