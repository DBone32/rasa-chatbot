import pymongo
import pandas as pd
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

channels = []
times = []
user = []
bot = []
intents = []
confidences = []

def add_row(channel='', time='', question='', answer='', intent='', confidence=''):
    channels.append(channel)
    times.append(time)
    user.append(question)
    bot.append(answer)
    intents.append(intent)
    confidences.append(confidence)

for conv in data:
    events = conv['events']
    timestamp = events[0]['timestamp']
    start_time = datetime.fromtimestamp(timestamp)
    if len(events) < 4:
        continue
    # print('{}. Conversation from {}'.format(start_time, conv['latest_input_channel']))
    add_row(channel=conv['latest_input_channel'], time=start_time)
    for event in events:
        intent = ''
        confidence = ''
        color = 'white'
        if 'parse_data' in event:
            color = 'blue'
            intent = event['parse_data']['intent']['name']
            confidence = event['parse_data']['intent']['confidence']
            # intent = '[{}({})]'.format(event['parse_data']['intent']['name'], event['parse_data']['intent']['confidence'])
        if 'text' in event:
            _from = event['event']
            _time = datetime.fromtimestamp(event['timestamp'])
            text = event['text']
            if _from == 'user':
                add_row(question=text, intent=intent, confidence=confidence, time=_time)
            else:
                add_row(answer=text, intent=intent, confidence=confidence, time=_time)
            # print(colored('     {}: {}{}'.format(event['event'].upper(), event['text'], intent).replace('\n', '   \n'), color))

data = {'chanel': channels, 'time': times, 'question': user, 'answer': bot, 'intent': intents, 'confidence': confidences}
df = pd.DataFrame(data)
df.to_csv('raw_data/conversations.csv', index=False, encoding='utf-8')