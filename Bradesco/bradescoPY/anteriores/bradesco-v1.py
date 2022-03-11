from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Bradesco/testePDF/Bradesco Intituto01 a 12 de 2020 (002) (3).pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open ("bradesco.csv", "w") as c:
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
            cab = re.findall(r'Entre [\d]{1,2}/[\d]{1,2}/[\d]{4} e [\d]{1,2}/[\d]{1,2}/[\d]{4}', line, flags=re.I)
            #print(cab)
            x= re.findall(r'Total|Data|valor disponivel|os dados acima|últimos lançamentos|[\d]{1,} of [\d]{1,2}',line, flags=re.I)
            #rod = re.findall(r'\“[a-z]{2,}.*[\s]{2,}', line, flags=re.I)
            #print(x,cab)

            date = re.findall(r"\b([\d]{1,2}/[\d]{1,2}/[\d]{4})\s\s",line)
            prelanc = re.split(r'\s{2,}', line.strip())           
            dcto = re.findall(r'\b([\d]{3,7})\b',line.strip())
            #print(dcto[0:1])
            valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}.',line.strip())
            valor = valores[0:1]
            #saldo = valores[-1:0] 
            
            '''if date:
                dcto = predcto[1:1]
            elif not date:
                dcto = predcto[0:1]

            dcto  = dcto[0] if dcto else '//'

            if not date:
                if prelanc[0] == dcto:
                    lanc = 'repete'
                elif prelanc[0] != dcto:
                    lanc = prelanc[0]
                
            elif date:
                if prelanc[1] != dcto:
                    lanc = prelanc[1]
                elif prelanc[1] == dcto:
                    lanc = 'repete'
                    '''
            if not date:
                if prelanc[0] == dcto[0:1]:
                    lanc = 0
                else:
                    lanc = prelanc[0]
            elif date:
                if prelanc[1] == dcto[1:1]:
                    lanc = 0
                else:
                    lanc = prelanc[1]
            else:
                lanc = 0
            #print(lanc)

            #print(date,dcto,lanc)

            date = date[0] if date else 0
            #lanc = lanc if lanc else 0
            dcto  = dcto[0] if dcto else '//'
            valor = valor[0] if valor else ''
            #saldo = saldo[0] if saldo else 0
            
            #print(date,lanc,dcto)
                        
            if cab:
                row = [date, lanc, dcto, valor, 'cabecalho']
            elif x:
                row = [date, lanc, dcto, valor, 'apagar linha']
            else:
                row = [date, lanc, dcto, valor]
            #print(row)
                                      
            '''while '' in row:
                row.remove('')'''

            ''''if lanc == 0:
                del row    
            elif not lanc in row:
                del row'''
            if row[-1] == 'apagar linha':
                del row
            else:
                table.append(row)
                #writer.writerow(row)
                #print(row)
            
    date = None
    j=None
    for i, row in enumerate(table):
        if row[0] != 0:
            date = row[0]
        elif row[0] == 0 and date:
            row[0] = 0
            if row[-1] == 'rodape':
                break
        if row[-1] == 'cabecalho':
            j = i
        print(row)

    table = table[j+2:i]
    writer.writerows(table)