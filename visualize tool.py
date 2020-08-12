import pymongo
from termcolor import colored
from datetime import datetime
from pymongo import MongoClient
client = MongoClient('18.140.240.198:27017',
                     username='ai_chatbot',
                     password='chatbot!@#',
                     authSource='tracker',
                     authMechanism='SCRAM-SHA-1')

db = client['tracker']
collection = db['conversations']
data = collection.find()
for conv in data:
    events = conv['events']
    timestamp = events[0]['timestamp']
    start_time = datetime.fromtimestamp(timestamp)
    if len(events) < 4:
        continue
    print('{}. Conversation from {}'.format(start_time, conv['latest_input_channel']))
    for event in events:
        intent = ''
        color = 'white'
        if 'parse_data' in event:
            color = 'blue'
            intent = '[{}({})]'.format(event['parse_data']['intent']['name'], event['parse_data']['intent']['confidence'])
        if 'text' in event:
            print(colored('     {}: {}{}'.format(event['event'].upper(), event['text'], intent).replace('\n', '   \n'), color))