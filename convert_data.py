import pandas as pd
import numpy as np
from unidecode import unidecode

def convert_IE():
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

def convert_utter():
    data = pd.ExcelFile('raw_data/chatbot.xlsx')
    outfile = open('data/utter.txt', 'w', encoding='utf-8-sig')
    actions = open('data/action.txt', 'w', encoding='utf-8-sig')
    out_intents = open('data/intents.txt', 'w', encoding='utf-8-sig')
    sheetnames = data.sheet_names[1:-1]
    for name in sheetnames:
        sheet_data = data.parse(name)
        answers = sheet_data['Answer']
        intents = sheet_data['Intent']
        current_intent = 0
        for idx, answer in enumerate(answers):
            intent = intents[idx]
            if intent != current_intent and type(intent) == str:
                out_intents.writelines(' - {}:\n'.format(intent))
                out_intents.writelines('     triggers: utter_{}\n'.format(intent))
                actions.writelines('- utter_{}\n'.format(intent))
                outfile.writelines('  utter_{}:\n'.format(intent))
                outfile.writelines('  - text: \"{}\"\n'.format(answer.replace('"', "'")))
                current_intent = intent
    outfile.close()

convert_utter()