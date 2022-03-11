from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Itau/Extrato Outubro.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open ("Extrato Outubro.csv", "w") as c:
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
            
        delete = re.findall(r'SALDO|SDO',line, flags = re.I)

        date = re.findall(r"([\d]{1,2} / [a-z]{3})",line)
        #print(date)
        lanc = re.findall(r'[\d]{1,2} / [a-z]{3}\s+(.+)[\s]{2,}[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line, flags=re.I)
        #print(lanc)
        dcto = re.findall(r'\b[\d]{6}\b',line)
        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line)
        valor = valores[0:1]
        #saldo = valores[-1:0]

        date = date[0] if date else 0
        lanc = str(lanc[0] if lanc else 0)
        dcto  = dcto[0] if dcto else 0
        valor = valor[0] if valor else 0
        #saldo = saldo[0] if saldo else 0

        lanc = str(lanc.strip() if lanc!=0 else 0)           

        row = [date, lanc, valor]
        #print(type(row[0]))
                
        while '' in row:
          row.remove('')
        
        if date == 0:
          del row
        elif 'SALDO' in row[1]:
          del row
        elif 'SDO' in row[1]:
          del row
        else:
          print(row)
          table.append(row)
          #writer.writerow(row) 
                
  #print(table)
  writer.writerows(table)