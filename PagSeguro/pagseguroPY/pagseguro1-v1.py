from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/PagSeguro').glob('*.pdf')) #/testePDF1

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
      lines = page.split('\n')

      for line in lines:
        date = re.findall(r"([\d]{1,2}-[\d]{1,2}-[\d]{4})",line)
        #print(date)
        prelanc = re.split(r'\s{1,}', line.strip())
        lanc = (' '.join(prelanc[3:-4])).strip()
        #print(lanc)
        #conta = prelanc[-4:]
        #print(conta)
        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3}[\.][\d]{0,2}',line)
        #print(valores)
        valor = prelanc[-3:]
        #print(valor)

        date = date[0] if date else 0
        lanc = lanc if lanc else 0
        #conta = conta[0] if conta else 0
        valor = valor[0] if valor else 0
        #print(valor)

        lanc = lanc.strip() if lanc!=0 else 0
        
        row = [date, lanc, valor]
        #print(row)
               
        while '' in row:
          row.remove('')
        
        if date == 0:
          del row
        elif lanc == 0:
          del row
        else:
          #print(row)
          table.append(row)
          #writer.writerow(row) 
                
    #print(table)
    writer.writerows(table)