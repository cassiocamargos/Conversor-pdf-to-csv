#from os import remove
from pathlib import Path
import pdftotext
import re
import csv
#import pandas as pd

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Inter/testePDF/inter.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open("inter.csv", "w") as c:
    writer= csv.writer(
        c,
        delimiter = ';',
        lineterminator = '\n'
    )

    with open(arq_extrato, "rb") as f:
        pdf = pdftotext.PDF(f)

    table = []

    for page in pdf:
        lines = page.split('\n')

        for line in lines:
            date = re.findall(r"([\d]{1,2}\/[\d]{1,2}\/[\d]{4})",line)
            prelanc = re.split(r'\s{2,}', line.strip())
            print(prelanc)
            #prelanc = re.split(r'[\d]{1,2}/[\d]{1,2}/[\d]{4}|.R\$ [\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}', line.strip())
            #lanc = prelanc[1:2]
            #dcto = re.findall(r'\b[\d]{6}\b',line)
            valores = re.findall(r'.R\$ [\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line)
            valor = valores[0:1]
            #saldo = valores[-1:0]

            if not date:
                lanc = prelanc[0:1]
            else:
                lanc = prelanc[1:2]

            date = date[0] if date else 0
            lanc = lanc[0] if lanc else 0
            #dcto  = dcto[0] if dcto else 0
            valor = valor[0] if valor else 0
            #saldo = saldo[0] if saldo else 0

            lanc = lanc.strip() if lanc!=0 else 0
            
            if not lanc:
                lanc = 0
            
            row = [date, lanc, valor]
            
            if date == 0:
                #del row
                pass
            else:
                print(row)
                table.append(row)
                #writer.writerow(row) 
                
    #print(table)
    writer.writerows(table)