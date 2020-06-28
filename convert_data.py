import pandas as pd
import numpy as np
from unidecode import unidecode

data = pd.ExcelFile('data/meeyland_data.xlsx')
sheet_names = data.sheet_names
intents = [unidecode(intent.lower().replace(' ', '_')) for intent in sheet_names]
dic = {}
for idx, intent in enumerate(intents):
    sheet_data = data.parse(sheet_names[idx])
    questions = sheet_data['Unnamed: 1']
    for question in questions:
        if type(question) != float and len(question) > 10:
            if intent not in dic:
                dic[intent] = []
            dic[intent].append(question)
train1_file = open('data/train1_nlu.md', 'w', encoding='utf-8-sig')
train2_file = open('data/train2_nlu.md', 'w', encoding='utf-8-sig')
test_file = open('data/test_nlu.md', 'w', encoding='utf-8-sig')
for intent in intents:
    train1_file.writelines('## intent:{}\n'.format(intent))
    train2_file.writelines('## intent:{}\n'.format(intent))
    test_file.writelines('## intent:{}\n'.format(intent))
    nlen = len(dic[intent])
    n_test = nlen//3
    n_train = nlen-n_test

    for i in range(n_train):
        train1_file.writelines(' - {}\n'.format(dic[intent][i]))
        if i < (n_train)/2:
            train2_file.writelines(' - {}\n'.format(dic[intent][i]))

    for i in range(n_train, nlen, 1):
        test_file.writelines(' - {}\n'.format(dic[intent][i]))