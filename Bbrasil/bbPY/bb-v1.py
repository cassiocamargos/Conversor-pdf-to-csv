from os import replace
from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Bbrasil').glob('*.pdf')) #/testePDF

for file in dir:    
  print('\n\n')
  
  namepdf = file.name
  print(namepdf)

  namecsv = file.name
  namecsv = namecsv[:-4] + '.csv'
  print(namecsv)

  with open(namecsv, "w", encoding = 'utf-8') as c:
    writer= csv.writer(
      c,
      delimiter = ';',
      lineterminator = '\n'
    )

    with file.open('rb') as f:    
      pdf = pdftotext.PDF(f)

    table = []

    for page in pdf:
      #print(page)
      lines = page.split('\n')

      for line in lines:
        rod = re.findall(r'S A L D O', line, flags=re.I)
        #print(rod)

        date = re.findall(r"([\d]{1,2}/[\d]{1,2}/[\d]{4})",line)
        #print(date)

        prelanc = re.split(r'\s{2,}', line.strip())
        #print(prelanc)       
        if not prelanc[3:4]:
          lanc = prelanc[0:1]
        #elif rod:
        #  lanc = rod
        else:
          lanc = prelanc[3:4]
        #print(lanc)
        x = re.findall(r'[\d]{4}\s[\d]{3}.*', line, flags=re.I)
        x = str(x[0] if x else '')
        x = x[:45]
        x = x.strip() if x!=0 else 0
        #print(x) 

        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}\s\w',line)
        valor = valores[0:1]
        #print(valor)
        
        if valor:
          if valor[0][-1] == 'C':
            valor[0] = valor[0][0:-2]
          elif valor[0][-1] == 'D':
            valor[0] = '-' + valor[0][0:-2]

        date = date[0] if date else ' - ' 
        lanc = lanc[0] if lanc else 0
        valor = valor[0] if valor else '0'

        lanc = lanc.strip() if lanc!=0 else 0
        
        if 'Cobrança referente'in lanc:
          date = ' - '
                
        if 'Saldo Anterior' in lanc:
          row = [date, lanc, valor, 'cabecalho']
        elif x:
          row = [date, x, valor]
        elif rod:
          row = [date, rod, valor, 'rodape']
        else:
          row = [date, lanc, valor]
        #print(row)
        
        if 'https'in row[1]:
          del row
        elif '' in row:
          del row
        elif lanc == date:
          del row
        else:
          #print(row)
          table.append(row)
          #writer.writerow(row) 

    date = None
    j=None
    for i, row in enumerate(table):
      if row[-1] == 'cabecalho':
        j=i

      if row[-1] == 'rodape':
        break
      #print(row)

    table = table[j:i]
    for x in table: print(x)
    writer.writerows(table)