def Color2Dico(ListColor):
    D={}
    for i in range(-3,0):
        D[i] = ListColor[i+3]
    for i in range(1,len(ListColor)-2):
            D[i] = ListColor[i+2]
    return D
