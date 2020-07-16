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


def convert_domain():
    df = pd.ExcelFile('raw_data/chatbot.xlsx')
    outfile = open('data/domain.yml', 'w', encoding='utf-8-sig')
    data = {}
    sheetnames = df.sheet_names[1:-1]
    for name in sheetnames:
        sheet_data = df.parse(name)
        answers = sheet_data['Answer']
        intents = sheet_data['Intent']
        current_intent = 0
        for idx, answer in enumerate(answers):
            intent = intents[idx]
            if intent != current_intent and type(intent) == str:
                data[intent] = answer.replace('"', "'")
                current_intent = intent

    # generate intents:
    outfile.writelines('intents:\n')
    for intent in data:
        if 'action_' in data[intent]:
            outfile.writelines('- {}:\n'.format(intent))
            outfile.writelines('    triggers: action_{}\n'.format(intent))
        elif type(data[intent]) != str:
            outfile.writelines('- {}\n'.format(intent))
        else:
            outfile.writelines('- {}:\n'.format(intent))
            outfile.writelines('    triggers: utter_{}\n'.format(intent))
    # generate entities:
    outfile.writelines('entities:\n')
    # generate slots:
    outfile.writelines('slots:\n')
    outfile.writelines('  requested_slot:\n    type: text\n')
    # generate responses:
    outfile.writelines('responses:\n')
    outfile.writelines('  utter_default:\n  - text: Xin lỗi mình không hiểu ý bạn ạ.\n')
    for intent in data:
        if type(data[intent]) == str and 'action_' not in data[intent]:
            outfile.writelines('  utter_{}:\n'.format(intent))
            outfile.writelines('  - text: "{}"\n'.format(data[intent]))
    # generate actions:
    outfile.writelines('actions:\n')
    outfile.writelines('- utter_default\n')
    for intent in data:
        if 'action_' in data[intent]:
            outfile.writelines(' - action_{}:\n'.format(intent))
        else:
            outfile.writelines(' - utter_{}:\n'.format(intent))
    outfile.close()

convert_domain()
