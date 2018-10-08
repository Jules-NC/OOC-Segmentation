def findCanonical(Parent, i):
      p = Parent[i]
      if p == -1: return i
      cx = findCanonical(Parent, Parent[i])
      Parent[i] = cx  # PATH COMPRESSION
      return cx


def union(Parent, cx, cy):  # cx<-cy <=> y devient le fils de x
    Parent[cy] = cx


def doQEBT(lV, E):
    # -1 = racine
    QEBTParent = [-1 for i in range(lV*2-1)]
    QEBT = [-1 for i in range(lV*2-1)]  # |V|-2 éléments
    size = lV
    for edge in E:
        child1 = edge[0]
        child2 = edge[1]
        c1 = findCanonical(QEBTParent, child1)
        c2 = findCanonical(QEBTParent, child2)
        if c1 == c2:
            continue
        union(QEBTParent, size, c1)
        union(QEBTParent, size, c2)
        QEBT[c1] = size
        QEBT[c2] = size
        size += 1
    print("  |QEBTParent:", QEBTParent)
    return QEBT
