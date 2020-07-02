import pandas as pd
import numpy as np
from unidecode import unidecode

data = pd.ExcelFile('raw_data/chatbot.xlsx')
outfile = open('data/nlu.md', 'w', encoding='utf-8-sig')
sheetnames = data.sheet_names[1:-1]
for name in sheetnames:
    sheet_data = data.parse(name)
    samples = sheet_data['Samples']
    intents = sheet_data['Intent']
    for idx, sample in enumerate(samples):
        if len(intents) > idx and type(intents[idx]) == str:
            outfile.writelines('\n## intent:{}\n'.format(intents[idx]))
        if type(sample) == str:
            outfile.writelines(' - {}\n'.format(sample))
outfile.close()