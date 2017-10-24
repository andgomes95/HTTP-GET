import os
nome = "exemplos/aaa"
casa = os.listdir(nome+"/")
for i in range (0,len(casa)):
    print casa[i]
