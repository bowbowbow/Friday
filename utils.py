import os
import numpy as np
from stanfordcorenlp import StanfordCoreNLP as nlp
from allennlp.predictors.predictor import Predictor
from selenium import webdriver


class PathSaver:
    """ Save the external path information """
    def __init__(self):
        self.parser_path = './stanford-corenlp-full-2018-10-05/'
        self.embed_path = './dat/glove.840B.300d.txt'
        self.driver_path = './dat/chromedriver.exe'
        self.allen_path = "https://s3-us-west-2.amazonaws.com/allennlp/models/srl-model-2018.05.25.tar.gz"


def get_stanford_parser(parser_path):
    """ Return the StanfordCoreNLP parser object """
    assert os.path.exists(parser_path)
    parser = nlp(parser_path)
    return parser


def get_allen_parser(parser_path):
    predictor = Predictor.from_path(parser_path)
    return predictor


def get_driver(driver_path):
    """ Return the Selenium chrome driver object """
    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(3)
    driver.get('https://google.com')
    return driver

def get_word_matrix(glove_path):
    """ Load word embedding matrix """
    map = dict()
    with open(glove_path, 'r', encoding='utf8') as f:
        ls = f.readlines()
        for idx,line in enumerate(ls):
            line = line.strip().split()
            try:
                assert len(line) == 301  # word embedding vector length + word
            except:
                continue
            vec = np.array([float(el) for el in line[1:]], dtype=np.float32)
            map[line[0]] = vec
    return map


def parse_allen_tag(words, tags):
    """
    Parse the allen-srl result into python list.
    Input:
        'words': ['enter', 'the', '"', 'ddehun', '"', 'in', '"', 'SearchBox', '"', '.']
        'tags': ['B-V', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'B-ARGM-LOC', 'I-ARGM-LOC', 'I-ARGM-LOC', 'I-ARGM-LOC', 'O']
    Output:
        parsed(dict): dictionary of 'tag':'word(s)' with merge BIO tag.
                example: {'ARG1': 'the " ddehun "', 'ARGM-LOC': 'in " SearchBox "', 'V': 'enter'}
    """
    parsed = dict()
    new_tag, tag_word = None, ''
    for word,tag in zip(words, tags):
        if tag == 'O':
            if new_tag is not None:
                parsed[new_tag] = tag_word.strip()
                continue
        tag = tag.split('-')
        if tag[0] == 'B':  # Meet the new Begin tag
            if new_tag is not None:  # Not the initial case
                parsed[new_tag] = tag_word.strip()
                tag_word = ''
            new_tag = '-'.join(tag[1:])
            tag_word += ' {}'.format(word)
        elif tag[0] == 'I':
            assert '-'.join(tag[1:]) == new_tag
            tag_word += ' {}'.format(word)
    return parsed


def check_user_generated_keyword(tok):
    if tok[0]!='"' and tok[-1] !='"':
        return False
    return True
