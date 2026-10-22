def Color2Dico(ListColor):
    D={}
    for i in range(1,len(ListColor) + 1):
        D[i] = ListColor[i-1]
    return D
