from os import replace
import pdftotext
from pathlib import Path
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/cassio-conversor/pdf/bradesco.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

'''with open ("bradesco.csv", "w") as c:
    writer= csv.writer(
        c,
        delimiter = ';',
        lineterminator = '\n'
    )'''

# Load your PDF
with open(arq_extrato, "rb") as f:
    pdf = pdftotext.PDF(f)

table = []

for page in pdf:
    lines = page.split('\n')

    for line in lines:
        #print(re.findall(r'\s+',line, flags=re.IGNORECASE))
        #print(line)
        date = re.findall(r"\b([\d]{1,2}/[\d]{1,2}/[\d]{4})\s\s",line)
        prelanc = re.split(r'\s{2,}', line.strip())
        #lanc = prelanc[1:2]
        dcto = re.findall(r'\s{2,}([\d]{3,7})\b',line)
        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}$',line)
        valor = valores[0:1]
        #saldo = valores[-1:0]     
        
        if not date:
            lanc = prelanc[0]
        elif date:
            lanc = prelanc[1]
        else:
            lanc = 0

        date = date[0] if date else 0
        #lanc = lanc[0] if lanc else 0
        dcto  = dcto[0] if dcto else 0
        valor = valor[0] if valor else 0
        #saldo = saldo[0] if saldo else 0

        '''if lanc == dcto:
            replace(lanc, 0)'''
        
        row = [date, lanc, dcto, valor]
        #print(row)

        while '' in row:
            row.remove('')
        

        if lanc == "Total":
            del row
        else:
            print(row)
            ##print()
            table.append(row)
            #writer.writerow(row)
        
        #table.append(row)
                
#print(table)
#writer.writerows(table)