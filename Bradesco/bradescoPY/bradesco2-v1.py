from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Bradesco/').glob('*.PDF')) #/testePDF

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
        #print(line)
        
        cab = re.findall(r'Entre [\d]{1,2}/[\d]{1,2}/[\d]{4} e [\d]{1,2}/[\d]{1,2}/[\d]{4}', line, flags=re.I)
        rod = re.findall(r'TOTAL DA MOVIMENTAÇÃO', line, flags=re.I)
        #print(rod)
        x= re.findall(r'Saldo Anterior|Total|Data|valor disponivel|os dados acima|últimos lançamentos|[\d]{1,} of [\d]{1,}',line, flags=re.I)

        date = re.findall(r"\b([\d]{2}/[\d]{2})\s",line)
        #print(date)
        prelanc = re.split(r'\s{2,}', line.strip())
        #print(prelanc)
        dcto = re.findall(r'\b([\d]{2,7})\s\s',line.strip())
        #print(dcto)
        valores = re.findall(r'[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}.',line.strip())
        valor = valores[0:1]
        
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

        date = date[0] if date else 0
        lanc = lanc if lanc else 0
        dcto  = dcto[0] if dcto else '//'
        valor = valor[0] if valor else ''
        
        if lanc == dcto:
          lanc = prelanc[0]
                    
        if cab:
          row = [date, lanc, dcto, valor, 'cabecalho']
        elif rod:
          row = [date, lanc, dcto, valor, 'rodape']
        elif x or lanc == 0:
          row = [date, lanc, dcto, valor, 'apagar linha']
        else:
          row = [date, lanc, dcto, valor]
        #print(row)

        if row[-1] == 'apagar linha':
          del row
        elif  not lanc:
          del row
        else:
          table.append(row)
          #print(row)
            
    date = None
    #j=0
    for i, row in enumerate(table):
      if row[0] != 0:
        date = row[0]
      elif row[0] == 0 and date:
        row[0] = date
        if row[-1] == 'rodape':
          break
      #if row[-1] == 'cabecalho':
      #  j = i
      #print(row)

    table = table[2:i]
    for x in table: print(x)
    writer.writerows(table)