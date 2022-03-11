from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/C6/testePDF/c6.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open ("c6.csv", "w") as c:
    writer= csv.writer(
        c,
        delimiter = ';',
        lineterminator = '\n'
    )

    with open(arq_extrato, "rb") as f:
        pdf = pdftotext.PDF(f, "0409")

    table = []

    for page in pdf:
        lines = page.split('\n')

        for line in lines:
            date = re.findall(r"([\d]{2}/[\d]{2}/[\d]{4})",line)
            #print(date)
            prelanc = re.split(r'[\d]{2}/[\d]{2}/[\d]{4}|\s{2,}', line.strip())
            lanc = prelanc[1:2]
            #print(lanc)
            valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}\s\w',line)
            valor = valores[0:1]
            
            if valor:
                if valor[0][-1] == 'C':
                    valor[0] = valor[0][0:-2]
                elif valor[0][-1] == 'D':
                    valor[0] = '-' + valor[0][0:-2]

            date = date[0] if date else 0 
            lanc = lanc[0] if lanc else 0
            valor = valor[0] if valor else 0

            lanc = lanc.strip() if lanc!=0 else 0
            
            row = [date, lanc, valor]
            
            if date == 0:
                del row
            elif 'SALDO' in lanc:
                del row
            elif '' in row:
                del row
            elif lanc == 'ABERTO':
                del row
            else:
                print(row)
                table.append(row)
                #writer.writerow(row) 

    #print(table)
    writer.writerows(table)   