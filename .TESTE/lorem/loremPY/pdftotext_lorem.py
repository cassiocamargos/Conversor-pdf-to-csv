# pdftotext -layout "nome_arquivo"

from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/.TESTE/EXTRATO_MENSAL_061021_145053.pdf') #/lorem/lorem_ipsum

with open(arq_extrato, "rb") as f:
    pdf = pdftotext.PDF(f)
print("".join(pdf))

    #arquivo = open ("text.txt", "r")
    #print(arquivo.read())
    #for line in arquivo :
    #    print(0)
  
'''# If it's password-protected
with open("secure.pdf", "rb") as f:
    pdf = pdftotext.PDF(f, "secret")'''

'''# How many pages?
print(len(pdf))'''

'''# Iterate over all the pages
for page in pdf:
    print(page)'''

'''#Read some individual pages
print(pdf[0])
print(pdf[1])'''

'''#Read all the text into one string
print("\n\n".join(pdf))'''