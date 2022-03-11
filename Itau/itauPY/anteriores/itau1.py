#import os
from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Itau/ITAÚ - Junho - Corretora.pdf')

with open ("ITAÚ - Junho - Corretora.csv", "w") as c:
    writer= csv.writer(
        c,
        delimiter = ';',
        lineterminator = '\n'
    )

    with open(arq_extrato, "rb") as f:
        pdf = pdftotext.PDF(f)

    table =[]
    for page in pdf:
        lines = page.split('\n')

        for line in lines:
            legenda = re.findall(r'A = agendamento|B = ações movimentadas|pela Bolsa de Valores|C = crédito a compensar|D = débito a compensar|G = aplicação programada|P = poupança automática|Para demais siglas, consulte as Notas|Explicativas no final do extrato', line, flags=re.M)
            #print(legenda)
            dt = re.findall(r'data',line)
            #print(dt)
            
            date = re.findall(r"\b([\d]{2}/[0-1][0-9])\b",line.strip())
            #print(date)
            prelanc = re.split(r'\s{2,}', line.strip())
            #print(prelanc)
            lanc2 = re.findall(r'\b[\d]{2}/[0-1][0-9]\b\s+([a-z]{3,}.*)\s+[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line.strip(), flags=re.I)
            #print(lanc2)
            #dcto = re.findall(r'\b[\d]{6}\b',line)
            valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}.',line.strip())
            #print(valores)
            valor = valores[0:1]
            #print(valor)
            #saldo = valores[-1:0] 

            if valor:
                    if valor[0][-1] == '':
                        valor[0] = valor[0][0:-1]
                    elif valor[0][-1] == '-':
                        valor[0] = '-' + valor[0][0:-1]
            #print(valor)

            if legenda:
                if not date and prelanc:
                    try: 
                        lanc = prelanc[1]
                    except IndexError:
                        pass
                elif date and len(prelanc)>=4:
                    try:
                        lanc = prelanc[2]
                    except IndexError:
                        pass
            else:
                if not date:
                    lanc = prelanc[0]
                elif date and len(prelanc)>=2:
                    lanc = lanc2[0].strip() if lanc2 else 0
                else:
                    lanc = 0

            date = date[0] if date else 0
            lanc2 = lanc2[0] if lanc2 else 0
            #dcto  = dcto[0] if dcto else 0
            valor = valor[0] if valor else 0
            #saldo = saldo[0] if saldo else 0
            
            lanc2 = str(lanc2.strip() if lanc2!=0 else 0)

            row = [date, lanc, valor]
            #print(row)

            '''while '' in row:
                row.remove('')'''

            if lanc =='SALDO APLIC AUT MAIS':
                del row
            elif lanc == 'Saldo anterior':
                del row
            elif not lanc:
                del row
            elif valor == 0:
                del row
            elif valor == 'siglas, ':
                del row
            else:
                table.append(row)
            #print(table)

    date = None
    j=None
    for i, row in enumerate(table):
        if row[0] != 0:
            date = row[0]
        elif row[0] == 0 and date:
            row[0] = date

            if row[1] == 'Saldo em C/C':
                break

        elif row[0] == 0:
            j=i
   
    table = table[j+1:i]
    for x in table: print(x)
    writer.writerows(table)