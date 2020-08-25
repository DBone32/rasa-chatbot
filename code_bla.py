import json

with open('results/intent_report.json') as f:
  data = json.load(f)

ex = ['micro avg', 'macro avg', 'weighted avg']
count = 0
precision = 0
recall = 0
f1 = 0
support = 0
for intent in data:
    if intent in ex:
        continue
    count += 1
    precision += data[intent]['precision']*data[intent]['support']
    recall += data[intent]['recall']*data[intent]['support']
    f1 += data[intent]['f1-score']*data[intent]['support']
    support += data[intent]['support']

print(precision/support)
print(recall/support)
print(f1/support)
print(support)