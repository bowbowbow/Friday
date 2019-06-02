import os
import time
from pprint import pprint
from nltk import Tree
from nltk.treeprettyprinter import TreePrettyPrinter
from utils import get_stanford_parser, PathSaver, get_driver, check_user_generated_keyword, get_allen_parser, parse_allen_tag
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
    new_clauses = []
    for clause in clauses:
        new_clause = []
        for tok in clause.split():
            if not check_user_generated_keyword(tok):
                tok = tok.lower()
            new_clause.append(tok)
        new_clauses.append(new_clause)

    new_clauses = [' '.join(clause) for clause in new_clauses]
    new_clauses = [clause + ' .' if clause[-1] != '.' else clause[:-1] + ' .' for clause in new_clauses]

    return new_clauses


def get_function_class(clause, nlp):
    """
    Read clause and return the Function class with assign the function type.
    Input:
        clause(str): one clause for function
        nlp(StanfordCoreNLP parser)
    Output:
        func: 'func' class with assignd function type
    """
    assert isinstance(clause, str)
    pos_tag_clause = nlp.pos_tag(clause)
    func = Func(clause, pos_tag_clause)
    func.assign_func_name()
    return func


def find_function_argument(func, allennlp):
    """
    Find argument of function call
    Input:
        func("Func" class): custom-class with assigned function type
    Output:
    """
    res = allennlp.predict(func.raw_clause)
    # TODO: Think about the issue that one verb per one clause is okay or not?
    # Has one verb and it should be same with prevous verb
    assert len(res['verbs']) == 1 and res['verbs'][0]['verb'] == func.func_word
    words, tags = res['words'], res['verbs'][0]['tags']
    assert len(words) == len(tags)
    parsed = parse_allen_tag(words, tags)
    pprint(parsed)
    func.find_func_target(parsed)
    func.find_func_argument(parsed)
    func.pretty_print()
    return func


def main_helper(element_tuple, language, nlp, allennlp, driver):
    """
    Main function of language part.
    Input:
        element_tuple(tuple): List of ('user-assign element name', 'element id for selector')
        language(str): user-generated natural language for test code
        driver: Selenium driver
    Output:
        codes: List of selenium code that are matched with 'language'
    """
    codes = []
    print("STEP0: Raw input\n{}\n".format(language))
    clauses = sent2clauses(language, nlp)
    print('STEP1: split language into clauses.\n{}\n'.format(clauses))
    funcs = [get_function_class(clause, nlp) for clause in clauses]
    print("STEP2: Assign the selenium function type for each of clauses.")
    for idx, f in enumerate(funcs): print("{}:{} => {}".format(idx, f.raw_clause, f.func_name))
    print("\nSTEP3: Find argument for each function.")
    funcs = [find_function_argument(func, allennlp) for func in funcs]
    print("\nSTEP4: Make Selenium code with name-tuple.")
    for func in funcs: func.make_selenium_code(element_tuple, driver)
    print("\nSTEP5: Run code!")
    for func in funcs: func.run_selenium_code()
    return funcs




if __name__ == '__main__':
    pathsaver = PathSaver()
    nlp = get_stanford_parser(pathsaver.parser_path)
    allennlp = get_allen_parser(pathsaver.allen_path)

    sample_sents = ['Refresh the website and move to "https://www.naver.com/".',
                    'Enter the "KAIST" in "SearchBox" and click the "Search" button', 'Wait the "3 seconds".']
    sample_tuple = [("SearchBox", 'q'), ("Search", 'btnK')]

    for sample_sent in sample_sents:
        driver = get_driver(pathsaver.driver_path)
        main_helper(sample_tuple, sample_sent, nlp, allennlp, driver)
