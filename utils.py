import os
from stanfordcorenlp import StanfordCoreNLP as nlp
from allennlp.predictors.predictor import Predictor
from selenium import webdriver


class PathSaver:
    """ Save the external path information """
    def __init__(self):
        self.parser_path = './stanford-corenlp-full-2018-10-05/'
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


def get_driver(driver_path, home_url='https://google.com'):
    """ Return the Selenium chrome driver object """
    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(1)
    driver.get(home_url)
    return driver

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
    if tok[0] != '"' and tok[-1] != '"':
        return False
    return True

def make_basic_code(raw_input, driver_path):
    code = ''
    code += 'from selenium import webdriver\n\n'
    raw_input = raw_input.replace('\n', ' ')
    code += "Input = '{}'\n\n".format(raw_input)
    code += 'driver_path = "'"{}"'"\n'.format(driver_path)
    code += 'driver = webdriver.Chrome(driver_path)\n'
    code += 'driver.implicitly_wait(1)\n'
    # code += "driver.get('https://google.com')\n"
    return code