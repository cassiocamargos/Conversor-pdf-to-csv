from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/.TESTE').glob('*.pdf'))

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
        #print(line)
        #prelanc = re.split(r'\s{2,}', line.strip())        
        dcto = re.findall(r'\b[\d]{4,7}\b',line)
        print(dcto)

        table.append(dcto)
          
    writer.writerows(table)