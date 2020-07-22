import pandas as pd
import numpy as np
from unidecode import unidecode
import re


def convert_IE():
    data = pd.ExcelFile('raw_data/chatbot-data.xlsx')
    outfile = open('data/nlu.md', 'w', encoding='utf-8-sig')
    sheetnames = data.sheet_names[:-1]
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
    df = pd.ExcelFile('raw_data/chatbot-data.xlsx')
    outfile = open('data/domain.yml', 'w', encoding='utf-8-sig')
    data = {}
    entities = []
    sheetnames = df.sheet_names[:-1]
    for name in sheetnames:
        sheet_data = df.parse(name)
        answers = sheet_data['Answer']
        intents = sheet_data['Intent']
        questions = sheet_data['Samples']
        current_intent = 0
        current_answer = 0
        for idx, answer in enumerate(answers):
            intent = intents[idx]
            if intent != current_intent and type(intent) == str:
                if type(answer) == float:
                    answer = current_answer
                data[intent] = answer.replace('"', "'")
                current_intent = intent
                current_answer = answer
        # find entities
        for question in questions:
            if type(question) == str:
                starts = [i+2 for i in range(len(question)) if question.startswith('](', i)]
                for start in starts:
                    end = question.find(')', start)
                    entity = question[start: end]
                    if entity not in entities:
                        entities.append(entity)
                    pass
    # read utter ask for required slot
    utter_ask = {}
    utter_ask_sheet = df.parse(df.sheet_names[-1])
    slots = utter_ask_sheet['Slots']
    utters = utter_ask_sheet['Utter_ask']
    for slot, utter in zip(slots, utters):
        utter_ask[slot] = utter

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
    for entity in entities:
        outfile.writelines('- {}\n'.format(entity))
    # generate slots:
    outfile.writelines('slots:\n')
    for entity in entities:
        outfile.writelines('  {}:\n'.format(entity))
        outfile.writelines('    type: text\n')
    outfile.writelines('  requested_slot:\n    type: text\n')
    # generate responses:
    outfile.writelines('responses:\n')
    outfile.writelines('  utter_default:\n  - text: "Xin lỗi mình không hiểu ý bạn ạ."\n')
    for intent in data:
        if type(data[intent]) == str and 'action_' not in data[intent]:
            outfile.writelines('  utter_{}:\n'.format(intent))
            outfile.writelines('  - text: "{}"\n'.format(data[intent]))
    for slot in utter_ask:
        outfile.writelines('  utter_ask_{}:\n'.format(slot))
        outfile.writelines('  - text: "{}"\n'.format(utter_ask[slot]))
    # generate actions:
    outfile.writelines('actions:\n')
    outfile.writelines(' - utter_default\n')
    for intent in data:
        if 'action_' in data[intent]:
            outfile.writelines(' - action_{}\n'.format(intent))
        else:
            outfile.writelines(' - utter_{}\n'.format(intent))




def convert_stories():
    df = pd.ExcelFile('raw_data/chatbot_data_core.xlsx')
    outfile = open('data/stories.md', 'w', encoding='utf-8-sig')
    sheetnames = df.sheet_names
    for i, name in enumerate(sheetnames):
        sheet_data = df.parse(name)
        stts = sheet_data['STT']
        users = sheet_data['User']
        bots = sheet_data['Bot']
        stories = sheet_data['Rasa-Stories']
        for idx, action in enumerate(stories):
            if stts[idx] == stts[idx] and stories[idx] == stories[idx]:
                if idx != 0 or i != 0:
                    outfile.writelines('\n')
                story_name = '## {} {}\n'.format(name, int(stts[idx]))
                outfile.writelines(story_name)
            if users[idx] == users[idx]:
                outfile.writelines('* {}\n'.format(action.strip()))
            elif bots[idx] == bots[idx]:
                outfile.writelines('  - {}\n'.format(action.strip()))
    outfile.close()

convert_stories()