import os
import json
import argparse
from pprint import pprint
import nltk
from utils import PathSaver, get_driver, check_user_generated_keyword, get_allen_parser, parse_allen_tag, make_basic_code
from func import Func

parser = argparse.ArgumentParser()
parser.add_argument("--run_selenium", type=bool, default=False, help='If True, also run selenium code. If False, only makes python output function.')
parser.add_argument("--use_corenlp", type=bool, default=False, help='')
args = parser.parse_args()


def sent2clauses(sent, parser):
    """
    Parse the sentence(str) into multiple clauses.
    One clause should be matched with one Selenium code.
    Input:
        sent(str): user-generated one raw sentence
        parser(StanfordCoreNLP or NLTK parser): Parser object
    Output:
        clauses(list of str): list of clauses(one Selenium code per clause)
    """
    # clauses = []
    # tree = parser.parse(sent)
    # res = nltk.Tree.fromstring(tree)

    # TODO: Find better ways to split the sentence into clauses, like parsing.
    while '\n' in sent: sent = sent.replace('\n', ' ')
    while 'And' in sent: sent = sent.replace('And', 'and')
    clauses = [clause.strip() for clause in sent.split('and')]
    final_clauses = []
    for clause in clauses: final_clauses += nltk.sent_tokenize(clause)
    clauses = final_clauses

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


def get_function_class(clause, nlp, run_selenium):
    """
    Read clause and return the Function class with assign the function type.
    Input:
        clause(str): one clause for function
        nlp(StanfordCoreNLP parser)
    Output:
        func: 'func' class with assignd function type
    """
    assert isinstance(clause, str)
    if args.use_corenlp:
        pos_tag_clause = nlp.pos_tag(clause)
    else:
        pos_tag_clause = nlp.pos_tag(nlp.word_tokenize(clause))
    func = Func(clause, pos_tag_clause, run_selenium)
    func.assign_func_name()
    return func


def find_function_argument(func, allennlp):
    """
    Find argument of function call (e.g. seconds for wait function)
    Input:
        func("Func" class): custom-class with assigned function type
    Output:
    """
    res = allennlp.predict(func.raw_clause)
    # TODO: Think about the issue that one verb per one clause is okay or not?
    # Has one verb and it should be same with prevous verb
    try:
        assert len(res['verbs']) == 1
    except:
        # TODO: Find better ways to solve this problem. If more than one verb, which one to choose?
        assert func.func_name == 'contain_value'
        res['verbs'] = [res['verbs'][0]]

    assert res['verbs'][0]['verb'] == func.func_word
    words, tags = res['words'], res['verbs'][0]['tags']
    assert len(words) == len(tags)
    parsed = parse_allen_tag(words, tags)
    pprint(parsed)
    func.find_func_target(parsed)
    func.find_func_argument(parsed)
    func.pretty_print()
    return func


def main_helper(selector_list, language, nlp, allennlp, driver, driver_path, run_selenium):
    """
    Main function of language part.
    Input:
        selector_list(list): list of dict(path, location, tagID)
        language(str): user-generated natural language for test code
        driver: Selenium driver
    Output:
        codes: List of selenium code that are matched with 'language'
    """
    codes = make_basic_code(language, './.' + driver_path)
    print("\n\n\nSTEP0: Raw input\n{}\n".format(language))
    clauses = sent2clauses(language, nlp)

    print('STEP1: split language into clauses.\n{}\n'.format(clauses))
    funcs = [get_function_class(clause, nlp, run_selenium) for clause in clauses]

    print("STEP2: Assign the selenium function type for each of clauses.")
    for idx, f in enumerate(funcs): print("{}:{} => {}".format(idx, f.raw_clause, f.func_name))

    print("\nSTEP3: Find argument for each function.")
    funcs = [find_function_argument(func, allennlp) for func in funcs]

    print("\nSTEP4: Make Selenium code with name-tuple.")
    for func in funcs: func.make_selenium_code(selector_list, driver)

    print("\nSTEP5: Run code! (Optional)")
    if run_selenium:
        for func in funcs: func.run_selenium_code()

    print('\nSTEP6: Make python code')
    for func in funcs: codes += func.code_string + '\n'
    num = len(os.listdir('./output/'))
    fname = './output/testfile_{}.py'.format(num)
    print("output file name: {}".format(fname))
    print('\n\noutput code: \n{}'.format(codes))

    # Write the generated code for debug
    if not os.path.exists('./output'): os.mkdir('./output')
    with open(fname, 'w') as f: f.write(codes)

    return funcs, codes


def local_main():
    """
    Main Function!
    make output file at /output/
    """
    # If True, also run selenium code. Else, only make output python file.
    run_selenium = args.run_selenium
    use_stanford_corenlp = args.use_corenlp
    pathsaver = PathSaver()
    if not use_stanford_corenlp:
        nlp = nltk
    else:
        from utils import get_stanford_parser
        nlp = get_stanford_parser(pathsaver.parser_path)
    allennlp = get_allen_parser(pathsaver.allen_path)

    sample_sents = ['Enter the "KAIST" in "SearchBox" and click the "Search" button',
                    'Wait the "3 seconds".',
                    'Refresh the website and move to "https://www.naver.com/".']
    sample_tuple = [("SearchBox", 'q'), ("Search", 'btnK')]
    # TODO: Change the above sample sents and tuple into Chrome extension output using 'read_extension_output()'

    for sample_sent in sample_sents:
        driver = get_driver(pathsaver.driver_path) if run_selenium else None
        main_helper(sample_tuple, sample_sent, nlp, allennlp, driver, pathsaver.driver_path, run_selenium)


def api_call_main(sample, pathsaver, run_selenium, nlp, allennlp):
    """
    API interaction main function.
    Input
        sample
        pathsaver
        run_selenium
        nlp
        allennlp
    Output
        code
    """
    driver = get_driver(pathsaver.driver_path) if run_selenium else None
    _, code = main_helper(sample['selectors'], sample['text'], nlp, allennlp, driver, pathsaver.driver_path, run_selenium)
    return code


def get_api_daemon_object():
    run_selenium = args.run_selenium
    use_stanford_corenlp = args.use_corenlp
    pathsaver = PathSaver()
    if not use_stanford_corenlp:
        nlp = nltk
    else:
        from utils import get_stanford_parser
        nlp = get_stanford_parser(pathsaver.parser_path)
    allennlp = get_allen_parser(pathsaver.allen_path)
    return run_selenium, use_stanford_corenlp, pathsaver, nlp, allennlp


def api_main():
    # TODO: Replace the below samples to to get Chrome extension output.
    samples = [{
      "selectors": [
        {
          "path": ".gLFyf",
          "location": "https://www.google.com/",
          "tagId": 1
        },
        {
          "path": "center:nth-child(1) > .gNO89b",
          "location": "https://www.google.com/",
          "tagId": 2
        }
      ],
        "text": 'open the "https://google.com" and wait the "4 seconds". And check "google" is on the page'}]

    run_selenium, use_corenlp, pathsaver ,nlp, allennlp = get_api_daemon_object()

    for sample in samples:
        code = api_call_main(sample, pathsaver, run_selenium, nlp, allennlp)

        # TODO: Replace this with post code to Chrome extension.
        pprint(code)


if __name__ == '__main__':
    api_main()



