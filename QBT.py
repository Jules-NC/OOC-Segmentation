def findCanonical(Parent, i):  # Pas de path compression
    p = Parent[i]
    if p == -1: return i
    cx = findCanonical(Parent, Parent[i])
    return cx


def union(Parent, cx, cy):  # cx<-cy <=> y devient le fils de x
    Parent[cy] = cx


def doQBT(lV, E):
    QBT = [-1 for i in range(lV * 2 - 1)]  # |V|-2 éléments
    size = lV  # Tout avant est un sommet => singleton
    for edge in E:
        child1 = edge[0]
        child2 = edge[1]
        c1 = findCanonical(QBT, child1)
        c2 = findCanonical(QBT, child2)
        if (c1 == c2): continue
        QBT[c1] = size
        QBT[c2] = size
        size += 1
    return QBT