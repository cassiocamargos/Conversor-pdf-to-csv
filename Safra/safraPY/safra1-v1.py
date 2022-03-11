from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Safra').glob('*.pdf')) #/testePDF1

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
        apagar = re.split(r'SALDO CONTA CORRENTE', line.strip())

        date = re.findall(r"([\d]{1,2}/[\d]{1,2})",line)
        #print(date)
        prelanc = re.split(r'\s{2,}', line.strip())
        prelanc = re.split(r'[\d]{1,2}/[\d]{1,2}/[\d]{4}\s*|\s{2,}', line.strip()) #|[\S]{,1}R\$\s[\S]{0,10}[\,]{0,1}[\d]{0,3}.[\d]{0,2}
        #print(prelanc)
        #print(prelanc)
        lanc = prelanc[1:2]
        #print(lanc)
        #dcto = re.findall(r'\b[\d]{6}\b',line)
        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line)
        valor = valores[0:1]
        #saldo = valores[-1:0]

        date = date[0] if date else 0
        lanc = lanc[0] if lanc else 0
        #dcto  = dcto[0] if dcto else 0
        valor = valor[0] if valor else 0
        #saldo = saldo[0] if saldo else 0

        lanc = lanc.strip() if lanc!=0 else 0
        
        row = [date, lanc, valor]
                
        #while '' in row:
        #  row.remove('')
        
        if date == 0:
          del row
        elif valor == 0:
          del row
        elif 'SALDO CONTA CORRENTE' in lanc:
          del row
        else:
          print(row)
          table.append(row)
          #writer.writerow(row) 
                
    #print(table)
    writer.writerows(table)