import json


def abc():
    with open('results/DIETClassifier_report.json', 'r') as json_file:
        text = json_file.read()
        json_data = json.loads(text)
        num_intents = 0
        for intent in json_data.keys():
            if intent in ['accuracy', 'macro avg', 'weighted avg', 'micro avg']:
                continue
            num_intents += 1
            print(intent)
        print(num_intents)
abc()

def statistics():
    with open('data/nlu.md', 'r') as file:
        lines = file.readlines()
        current_intents = ""
        dics = {}
        for line in lines:
            if '## intent:' in line:
                current_intents = line.replace('## intent:', '')
                if current_intents not in dics:
                    dics[current_intents] = []
            if ' - ' in line:
                line = line.replace(' - ', '')
                dics[current_intents].append(line)
        print(dics)
        res_dict = {}
        for intent in dics:
            if '/' in intent:
                f1, f2 = intent.split('/')
                if f1 not in res_dict:
                    res_dict[f1] = {}
                if f2 not in res_dict[f1]:
                    res_dict[f1][f2] = []
                res_dict[f1][f2].append(dics[intent])
        for intent in res_dict:
            print('{}:{}'.format(intent, len(res_dict[intent])))
