import os
from nltk import Tree
from utils import get_stanford_parser
from func import Func


def sent2clauses(sent, parser):
    """
    Parse the sentence(str) into multiple clauses.
    One clause should be matched with one Selenium code.
    Input:
        sent(str): user-generated one raw sentence
        parser(StanfordCoreNLP parser): Parser object
    Output:
        clauses(list of str): list of clauses(one Selenium code per clause)
    """
    clauses = []
    tree = parser.parse(sent)
    res = Tree.fromstring(tree)

    # TODO: Find better ways to split the sentence into clauses, like parsing.
    clauses = [clause.strip() for clause in sent.split('and')]
    return clauses


def get_function_class(clause, nlp):
    """
    Read clause and return the Function class with assign the function type.
    """
    pos_tag_clause = nlp.pos_tag(clause)
    func = Func(clause, pos_tag_clause)
    func.assign_func_name()
    return


def find_function_argument(clause, func):
    """
    Find argument of function call
    Input:
        clause(str): user-generated string that indicates the one Selenium function.
        func("Func" class): custom-class to
    Output:
    """


if __name__ == '__main__':
    parser_path = './stanford-corenlp-full-2018-10-05/'
    nlp = get_stanford_parser(parser_path)
    sample_sent = 'Enter the "ddehun" in "SearchBox".'
    print(nlp.pos_tag(sample_sent))
    input()
    res = sent2clauses(sample_sent, nlp)
    print(res)