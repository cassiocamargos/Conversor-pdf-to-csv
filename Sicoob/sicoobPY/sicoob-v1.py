from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Sicoob/').glob('*.pdf')) #/testePDF

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
        date = re.findall(r"([\d]{1,2}/[\d]{1,2})",line)
        prelanc = re.split(r'(\s{1,})([\d]{1,2}/[\d]{1,2})', line.strip())
        #print(prelanc)
        lanc = prelanc[0:1]
        #lanc = re.findall(r'[\d]{1,2}/[\d]{1,2}\s+(.+)(?=[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}.\b)',line, flags=re.I) #(.+)(?=\s+[\d]{6})
        #lanc = lanc[0:1]
        #print(lanc)
        #dcto = re.findall(r'\b[\d]{6}\b',line)
        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}.',line)
        valor = valores[0:1]
        #saldo = valores[-1:0]
        
        if valor:
          if valor[0][-1] == 'C':
            valor[0] = valor[0][0:-1]
          elif valor[0][-1] == 'D':
            valor[0] = '-' + valor[0][0:-1]

        date = date[0] if date else 0 
        lanc = lanc[0] if lanc else 0
        #print(lanc)
        valor = valor[0] if valor else 0
        #saldo = saldo[0] if saldo else 0

        lanc = lanc.strip() if lanc!=0 else 0
        
        row = [date, lanc, valor]
        
        '''if date == 0:
          if lanc == 'C' or lanc == 'D':            
            table.append(row)
          else:
            del row
        else:       ''' 
        print(row)
        table.append(row)
        #writer.writerow(row) 

    writer.writerows(table)