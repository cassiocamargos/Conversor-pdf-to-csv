from pathlib import Path
import pdftotext
import re
import csv

dir = sorted(Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/Sisloc/').glob('*.pdf')) #/testePDF

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
        x = re.findall(r'Qt:|Data da Liquidação:',line, flags=re.I)
        #print(x)

        date = re.findall(r"([\d]{1,2}/[\d]{1,2}/[\d]{1,2})",line)
        #print(date[:])
        emissao = date[:1]
        #print(emissao)
        venc = date[1:2]
        #print(venc)
        liquid = date[-1:]
        #print(liquid)

        emissao = emissao[0] if emissao else 0
        venc = venc[0] if venc else 0
        liquid = liquid[0] if liquid else 0
        #print(emissao, venc, liquid)


        prelanc = re.split(r'BOLETO|Transfer*', line.strip())
        #print(prelanc[:1])
        lanc = prelanc[0:1]
        #print(lanc)

        lanc = lanc[0] if lanc else 0
        lanc = lanc.strip() if lanc!=0 else 0


        valores = re.findall(r'\d[\S]{0,10}[\.]{0,1}[\d]{0,3},[\d]{0,2}',line)
        #print(valores[:])
        valor = valores[0:1]
        #print(valor)
        acr = valores[1:2]
        #print(acr)
        des = valores[2:3]
        #print(des)
        total = valores[-1:]
        #print(total)

        valor = valor[0] if valor else 0
        acr = acr[0] if acr else 0
        des = des[0] if des else 0
        total = total[0] if total else 0
        #print(valor, acr, des, total)
			
				
        #row = [lanc, emissao, venc, liquid, valor, acr, des, total, 'apagar linha']
				        
        row = [lanc, emissao, venc, liquid, valor, acr, des, total]
	

        print(row)
        table.append(row)
        #writer.writerow(row) 

    writer.writerows(table)