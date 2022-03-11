from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Itau').glob('*.pdf')) #/testePDF3

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