import os
from stanfordcorenlp import StanfordCoreNLP as nlp
from selenium import webdriver


def get_stanford_parser(parser_path):
    """ Return the StanfordCoreNLP parser object """
    assert os.path.exists(parser_path)
    parser = nlp(parser_path)
    return parser


def get_driver(driver_path):
    """ Return the Selenium chrome driver object """
    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(3)


