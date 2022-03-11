from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Itau/testePDF/itau3.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open ("itau3.csv", "w") as c:
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
            date = re.findall(r"([\d]{1,2}/[\d]{1,2}/[\d]{4})",line)
            #print(date)
            lanc = re.findall(r'([a-z].+)\s+. R\$ [\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line, flags=re.I)
            valor = re.findall(r'. R\$ [\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line)

            date = date[0] if date else 0
            lanc = lanc[0] if lanc else 0
            valor = valor[0] if valor else 0

            lanc = lanc.strip() if lanc!=0 else 0
            
            if date:
                row = [date]
            else:
                row = [lanc, valor]
                    
            while '' in row:
                row.remove('')

            if row[0] == 'saldo do dia':
                del row
            elif row[0] ==0:
                del row
            else:
                print(row)
                table.append(row)
                #writer.writerow(row) 
                
    #print(table)
    writer.writerows(table)