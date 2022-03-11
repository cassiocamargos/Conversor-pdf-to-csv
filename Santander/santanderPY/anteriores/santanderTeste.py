from os import remove
import pdftotext
import re
import csv

with open("/mnt/c/users/legalização/documents/python/testes/pdf/santander.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

for page in pdf:
    lines = page.split('\n')

    table=[]

    for line in lines:
        
        row = re.split(r'\s{2,}', line.strip())
        while '' in row:
            row.remove('')
        
        
        
        
        # replace trailing spaces with comas
        row=re.sub('  +','_',line)
        # reducing the number of comas to one
        row=[cols.strip() for cols in re.sub('_+','_',row).split('_')]
        # handling missed separators
        #row= ','.join(row).replace('  ',',').split(',')
        # append row to table
        table.append(row)

        print(row)
        

    '''with open ("bradesco.csv", "w") as c:
        writer= csv.writer(c)
        writer.writerows(table)'''