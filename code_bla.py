import json
from tqdm import tqdm
import time


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


def send_request():
    import requests
    data = json.dumps({"sender": 'tester1',"message": "Tôi muốn đầu tư vào meeyland thì làm thế nào"})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
    res = res.json()
    print(res)


def delete_all_data_in_mongodb():
    from pymongo import MongoClient
    client = MongoClient('18.140.240.198:27017',
                         username='ai_chatbot',
                         password='chatbot!@#',
                         authSource='tracker',
                         authMechanism='SCRAM-SHA-1')

    db = client['tracker']
    collection = db['conversations']
    data = collection.find()
    for dat in tqdm(data):
        query = {'_id': dat['_id']}
        collection.delete_one(query)


def delete_all_data_in_test_posgresql():
    import psycopg2
    # connection = psycopg2.connect(user="postgres",
    #                               password="dbpass",
    #                               host="localhost",
    #                               port="5432",
    #                               database="ai-chatlog")
    connection = psycopg2.connect(user="ai-chatlog-user", password="QUktQ2hhdExvZy10ZXN0Cg==", host="10.10.22.9",
                                  port="5432",
                                  database="ai-chatlog")
    cursor = connection.cursor()
    table = ['message_log', 'conversation_event',
             'conversation_action_metadata',
             'conversation_entity_metadata',
             'conversation_intent_metadata',
             'conversation_session',
             'conversation_policy_metadata',
             'conversation']
    for tab in table:
        cursor.execute('DELETE FROM {} WHERE true'.format(tab))
    connection.commit()


def test_cuda():
    import tensorflow as tf
    tf.test.is_gpu_available(cuda_only=True, min_cuda_compute_capability=None)


def get_meeychat_data():
    import time
    import pymongo
    import requests
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    myclient = pymongo.MongoClient("mongodb://10.10.20.169:27017/")
    mydb = myclient["meeychat"]
    mycol = mydb["rocketchat_message"]
    x = mycol.find().sort("ts")
    room_data = {}
    for data in x:
        if 'rid' not in data:
            continue
        room_id = data['rid']
        username = data['u']['username']
        if room_id not in room_data and username=='cskhmeeyland':
            continue
        msg = data['msg']
        if room_id not in room_data:
            room_data[room_id] = {'messages': [{'username': username, 'msg': []}]}
            room_data[room_id]['is_cskh'] = False
            room_data[room_id]['ignore'] = False
        last_sender = room_data[room_id]['messages'][-1]['username']
        if username != last_sender:
            room_data[room_id]['messages'].append({'username': username, 'msg': [msg]})
        else:
            room_data[room_id]['messages'][-1]['msg'].append(msg)
        if 'màu đỏ' in msg or "bị che" in msg or msg == "":
            room_data[room_id]['ignore'] = True
        if 'cskh' in username:
            room_data[room_id]['is_cskh'] = True

    # init posgresql connect
    import psycopg2
    # connection = psycopg2.connect(user="postgres", password="dbpass", host="localhost", port="5432", database="ai-chatlog")
    connection = psycopg2.connect(user="ai-chatlog-user", password="QUktQ2hhdExvZy10ZXN0Cg==", host="10.10.22.9", port="5432",
                                  database="ai-chatlog")
    cursor = connection.cursor()
    # insert data
    for room_id in tqdm(room_data):
        if room_data[room_id]['ignore']:
            continue
        if room_data[room_id]['is_cskh']:
            time_str = str(time.time()).replace('.', '')
            conv_id = "{}_{}".format(room_id, time_str)
            print('Room ID: {}'.format(room_id))
            for data in room_data[room_id]['messages']:
                username, msgs = data['username'], data['msg']
                if 'cskh' in username:
                    cskh_text = '\n'.join(msgs)
                    time.sleep(0.5)
                    timestamp = get_timestamp(cursor, conv_id)
                    insert_msg_to_db("CSKH: {}".format(cskh_text), timestamp, conv_id, cursor, connection)
                    print('     cskh: {}'.format(cskh_text))
                else:
                    user_text = '. '.join(msgs)
                    data = json.dumps({"sender": conv_id, "message": user_text})
                    res = requests.post('https://ai-chatbot-api-test.meey.dev/webhooks/rest/webhook', data=data, headers=headers)
                    print('     user: {}'.format(user_text))


def get_timestamp(cursor, conv_id):
    try:
        cursor.execute("SELECT timestamp FROM conversation_event where conversation_id='{}' and type_name='action'".format(conv_id))
        timestamps = cursor.fetchall()
        timestamp1 = max(timestamps)[0]
        cursor.execute("SELECT timestamp FROM conversation_event where conversation_id='{}' and type_name='bot'".format(conv_id))
        timestamps = cursor.fetchall()
        timestamp2 = max(timestamps)[0]
        timestamp = (timestamp1 + timestamp2)/2
    except:
        timestamp = 0.0
    return timestamp


def insert_msg_to_db(msg, timestamp, conv_id, cursor, connection):
    msg = json.dumps(msg).replace('\"', '')
    data = '{"sender_id": "{conv_id}", "event": "bot", "timestamp": "{timestamp}", "text": "{msg}", "data": {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, "metadata": {}}'
    data = data.replace('{conv_id}', conv_id)
    data = data.replace('{timestamp}', str(timestamp))
    data = data.replace('{msg}', msg)
    cursor.execute(
        "INSERT INTO conversation_event (conversation_id,type_name,timestamp,intent_name,action_name,policy,is_flagged,data,evaluation,rasa_environment,slot_name,slot_value) VALUES ('{}', 'bot', {}, null, null, null, false, '{}',null, 'production', null, null)".format(
            conv_id,
            str(timestamp),
            data)
    )
    connection.commit()


if __name__ == "__main__":
    get_meeychat_data()