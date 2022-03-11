from pathlib import Path
import pdftotext
import re
import csv

arq_extrato = Path('/mnt/c/Users/AiO-04/documents/Cassio/Conversor/pdf/TESTE/extratotocsv/testePDF/extratoTeste.pdf')

'''arq_extrato.name
print(arq_extrato.name)'''

with open(arq_extrato, "rb") as f:
    pdf = pdftotext.PDF(f)