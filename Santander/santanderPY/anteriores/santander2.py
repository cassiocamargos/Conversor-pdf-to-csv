#from os import remove
from os import replace
from pathlib import Path
import pdftotext
import re
import csv
import pandas as pd

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Santander/testePDF/santander2.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open ("santander2.csv", "w") as c:
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
          line = line.replace('  -  ', '000000')

          cab = re.findall(r'\*[a-z]{4,}.*', line, flags=re.I)
          rod = re.findall(r'\“[a-z]{2,}.*', line, flags=re.I)
          x= re.findall(r'SALDO EM [\d]{2}/[0-1][0-9]|Data|Créditos|extrato.*[\d]{1,2}/[\d]{1,2}/[\d]{4}|[a-z]{4,}.*PIM..',line, flags=re.I)
          #print(x,cab,rod)

          predate = re.findall(r"\b([\d]{2}/[0-1][0-9])\s\s",line.strip())
          date = predate[0:1]
          #print(date)

          prelanc = re.split(r'\s{2,}', line.strip())
          lanc2 = re.findall(r'\b[\d]{2}/[0-1][0-9]\b\s+([a-z]{3,}.*)\s+\b[\d]{6}\b',line.strip(), flags=re.I)

          dcto = re.findall(r'(\b[\d]{6}\b)',line)
          #print(date, dcto)

          valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}.',line.strip())
          valor = valores[0:1]
          #saldo = valores[-1:0] 

          if valor:
                  if valor[0][-1] == '':
                      valor[0] = valor[0][0:-1]
                  elif valor[0][-1] == '-':
                      valor[0] = '-' + valor[0][0:-1]
          #print(valor)

          '''if not date:
              lanc = prelanc[0]
          elif date:
              lanc = prelanc[1]
          else:
              lanc = 0'''

          if not date:
              lanc = prelanc[0]
          elif date and len(prelanc)>=2:
              lanc = lanc2[0].strip() if lanc2 else 0
          else:
              lanc = 0
          #print(date,dcto,lanc)

          date = date[0] if date else 0
          #lanc = lanc if lanc else 0
          dcto  = dcto[0] if dcto else '//'
          valor = valor[0] if valor else ''
          #saldo = saldo[0] if saldo else 0
          
          #lanc2 = lanc2.strip() if lanc2!=0 else 0
          
          if cab:
              row = [date, lanc, dcto, valor,'cabecalho']
          elif rod:
              row = [date, lanc, dcto, valor, 'rodape']
          elif x:
              row = [date, lanc, dcto, valor, 'apagar linha']
          else:
              row = [date, lanc, dcto, valor]
          #print(row)
          
          delete = re.findall(r'SALDO ANTERIOR|SALDO ATUAL',line,flags=re.I)
          quebra = re.findall(r'Saldos por Período', line)
          #print(delete, quebra)
              
          while '' in row:
              row.remove('')

          if lanc in row == delete:
              del row
          elif not lanc in row:
              del row
          elif row[-1] == 'apagar linha':
              del row
          elif not valor:
              del row
          else:
              table.append(row)
              #print(row)
          
  date = None
  j=None
  for i, row in enumerate(table):
      if row[0] != 0:
          date = row[0]
      elif row[0] == 0 and date:
          row[0] = date

          if row[-1] == 'rodape':
              break

      if row[-1] == 'cabecalho':
          j=i
      #print(row)

  table = table[j:i]
  for x in table: print(x)
  writer.writerows(table)