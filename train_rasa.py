import logging
import pprint
from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_nlu.model import Interpreter
from rasa_nlu.test import run_evaluation


logfile = 'nlu_model.log'


def train_nlu(train_path, test_path, configs, model_path):
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    training_data = load_data(train_path)
    trainer = Trainer(config.load(configs))
    trainer.train(training_data)
    model_directory = trainer.persist(model_path, project_name='current', fixed_model_name='nlu')
    result = run_evaluation(test_path, model_directory)
    predictions = result['intent_evaluation']['predictions']
    for predict in predictions:
        print('{}:{}-{}'.format(predict['text'], predict['intent'], predict['confidence']))

    print('Acc: {}'.format(result['intent_evaluation']['accuracy']))
    print('F1 : {}'.format(result['intent_evaluation']['f1_score']))
    print('Pre: {}'.format(result['intent_evaluation']['precision']))

def run_nlu(nlu_path):
    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    interpreter = Interpreter.load(nlu_path)
    pprint.pprint(interpreter.parse("Share some latest news around the world?"))
    pprint.pprint(interpreter.parse("What is going on in technology?"))
    pprint.pprint(interpreter.parse("What is going on in education?"))


if __name__ == '__main__':
    train_nlu('./data/train2_nlu.md', './data/test_nlu.md', 'config.yml', './models')
    # run_nlu('./models/current/nlu')