def generate_tokens(path):
    with open(path, 'r') as fp:
        buf = []
        while True:
            ch = fp.read(1)
            if ch == '':
                break
            elif ch.isspace():
                if buf:
                    yield ''.join(buf)
                    buf = []
            else:
                buf.append(ch)

if __name__ == '__main__':
    liste = []
    for token in generate_tokens('SienneJC.graph'):
        liste.append(token)   
    print("Fin lecture")
    i=0
    passer = 1
    nbLigne = int(liste[3])
    nbColonne = int(liste[1])
    weight = [0] * int(liste[5])
    while (i<len(liste)):
        if passer == 0 :
            temp=int(liste[i])
            temp2=int(liste[i+1])
            i=i+2
            if temp>temp2 :
                swap=temp2
                temp2 = temp
                temp = swap
            if (temp2-temp)==1:
                res = (temp2//nbColonne)*(nbColonne)+(temp2//nbColonne)*(nbColonne-1)+(temp2%nbColonne)-1
                weight[res] = float(liste[i])
            else:
                res = (temp2//nbColonne)*(nbColonne-1)+(temp2%nbColonne)+((temp2//nbColonne)-1)*nbColonne
                weight[res] = float(liste[i])
                
        if (liste[i]=='values'):
            passer = 0
        i=i+1
    print("Weight initialisé")