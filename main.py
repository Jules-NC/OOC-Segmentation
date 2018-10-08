import pandas as pd
import QEBT
import QBT
import GraphPrinter

lV = 8 # |V|
E = [(0, 1), (1,2), (2,3), (3,7), (7,6), (6,5), (5,4), (4, 0), (1,5), (2,6)]
F = [2, 2, 0, 1, 0, 2, 1, 0, 2, 3]

# Tri de F par ordre croissant, E suit
F, E = zip(*sorted(zip(F, E)))


GraphPrinter.view(E, F)

print("|v|:", lV)
QBT = QBT.doQBT(lV, E)
print("VERIF:", QBT == [9,13,8,8,9,12,10,10,11,12,11,14,13,14,-1], QBT, "\n")
QEBT = QEBT.doQEBT(lV, E)
print("VERIF:", QEBT == QBT, QEBT)
GraphPrinter.viewP(QEBT)