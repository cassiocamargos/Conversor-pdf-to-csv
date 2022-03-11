from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Inter').glob('*.pdf')) #/testePDF

''' PASSANDO PELOS ARQUIVOS DO DIRETORIO '''
for file in dir:    
  print('\n\n')
  
  ''' LENDO NOME DO ARQUIVO '''
  namepdf = file.name
  print(namepdf)

  ''' RENOMEANDO COM EXTENSAO .CSV'''
  namecsv = file.name
  namecsv = namecsv[:-4] + '.csv'
  print(namecsv)

  ''' ESCREVENDO CSV '''
  with open(namecsv, "w", encoding = 'utf-8') as c:
    writer= csv.writer(
    c,
    delimiter = ';',
    lineterminator = '\n'
    )

    ''' LENDO O PDF '''
    with file.open('rb') as f:    
      pdf = pdftotext.PDF(f)

    table = []

    for page in pdf:
      lines = page.split('\n')

      for line in lines:
        date = re.findall(r'([\d]{1,2}\/[\d]{1,2}\/[\d]{4})',line)
        prelanc = re.split(r'[\d]{1,2}/[\d]{1,2}/[\d]{4}\s*|\s{2,}', line.strip()) #|[\S]{,1}R\$\s[\S]{0,10}[\,]{0,1}[\d]{0,3}.[\d]{0,2}
        #print(prelanc)
        valores = re.findall(r'[\S]{,1}R\$\s[\S]{0,10}[\,]{0,1}[\d]{0,3}.[\d]{0,2}',line) #VERIFICAR PONTUAÇÃO DOS VALORES
        valor = valores[0:1]
        #valor = prelanc[-2:-1]
        #print(valor)

        if prelanc[0] == '':
          lanc = prelanc[1:2]
        else:
          lanc = prelanc[0:1]

        date = date[0] if date else 0
        #print(date)
        lanc = lanc[0] if lanc else 0
        #print(lanc)
        valor = valor[0] if valor else 0
        #print(valor)

        lanc = lanc.strip() if lanc!=0 else 0
        
        row = [date, lanc, valor]        
        
        print(row)
        table.append(row)
        #writer.writerow(row) 
                
    #print(table)
    writer.writerows(table)