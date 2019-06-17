import os
import pickle
import time
import operator
import numpy as np

class KeywordManager:
    def __init__(self):
        self.func2keyword = {
            'click':['click', 'touch', 'press'],
            'wait':['wait', 'sleep'],
            'write':['enter', 'put', 'write', 'feed', 'input'],
            'contain_value': ['have', 'has', 'contain', 'check'],
            'refresh':['refresh', 'reload'],
            'move_url': ['go', 'move', 'open']
        }
        self.keyword_list = [el for li in self.func2keyword.values() for el in li]
        assert len(self.keyword_list) == len(list(set(self.keyword_list)))
        self.keyword2func = {}
        for k, vlist in self.func2keyword.items():
            for v in vlist:
                self.keyword2func[v] = k  # reverse of func2keyword for each keyword


class Func:
    def __init__(self, clause, pos_tag_clause, run_selenium):
        self.keyman = KeywordManager()
        self.func_name = None
        self.func_word = None
        self.target_name = None
        self.need_arguments = False
        self.arguments_list = []
        self.raw_clause = clause
        self.pos_tag_clause = pos_tag_clause
        self.selenium_func, self.selenium_argument = None, None
        self.code_string = ''
        self.embed_manager = None  # Lazy loading only when need
        self.run_selenium = run_selenium

    def pretty_print(self):
        """
        Print the result of function type, argument or target pretty for debug.
        """
        print('-' * 30)
        print("Raw Input: {}".format(self.raw_clause))
        print("Function Type and word: {}  {}".format(self.func_name, self.func_word))
        if self.target_name is not None:
            print("Target Name: {}".format(self.target_name))
        if len(self.arguments_list) != 0:
            print("Argument Names: {}".format(self.arguments_list))
        print('-' * 30)

    def assign_func_name(self):
        """
        Assign the function type by keyword matching with verb word in clause.
        If clause's verb doesn't exists in keyword, use w2v to find the most similar keyword and assign it.
        If there are more than one verb, how to deal with?
        """

        # TODO: Implement the better way to find the " Verb". (e.g. parse the clause and select the main verb)
        find_keyword = False
        verb_list = []
        for (word,tag) in self.pos_tag_clause:
            if tag[0] == 'V':
                verb_list.append(word)
            if word in self.keyman.keyword_list:
                if find_keyword:
                    raise ValueError("More than one keyword is exists, {} and {}".format(self.func_word, word))
                find_keyword = True
                self.func_word = word
                self.func_name = self.keyman.keyword2func[word]
                if self.func_name in ['write', 'wait']: self.need_arguments = True

        # Exact match with keyword is failed. Use word embedding similarity for decision.
        if not find_keyword:
            print("[Warning] Use word embedding to decide the function type")
            self.embed_manager = EmbedManager()
            score_save = dict()
            if len(verb_list) == 0: raise ValueError("No keyword and verb to decide the function type.")
            for verb in verb_list:
                scores = self.embed_manager.get_func_by_emb(verb)
                for k in scores:
                    if k in score_save: score_save[k] += score_save[k]
                    else: score_save[k] = scores[k]
                scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
                self.func_word = verb_list[0]
                self.func_name = scores[0][0]
                if self.func_name in ['write', 'wait']: self.need_arguments = True

    def find_func_target(self, parsed):
        """
        Find the target element that is affected by function and should be specified before function call.
        For example, 'Click' function should find the button to be clicked.
        Input:
            parsed: srl-parsed result
        Output:
            boolean: If function type needs some target instance(e.g. clicked button), return True. Else (e.g. wait,
                     refresh) return False
        """

        # TODO: Run and expand with more test case
        if self.func_name == 'click':
            self.target_name = parsed['ARG1']
        elif self.func_name == 'write':
            self.target_name = parsed['ARGM-LOC']
        else:
            pass

    def find_func_argument(self, parsed):
        """
        Find the argument of function and mark it (e.g. text of 'write' function to write)
        Input:
            parsed: srl-parsed result
        """
        if self.func_name == 'click':
            pass
        elif self.func_name == 'wait':
            arg = parsed['ARGM-TMP'] if 'ARGM-TMP' in parsed else parsed['ARG1']
            self.arguments_list.append(arg)
        elif self.func_name == 'write':
            arg = parsed['ARG1'] if 'ARG1' in parsed else parsed['ARG0']
            self.arguments_list.append(arg)
        elif self.func_name == 'contain_value':
            arg = parsed['ARG1']
            self.arguments_list.append(arg)
        elif self.func_name == 'refresh':
            self.arguments_list.append(parsed['ARG1'])
        elif self.func_name == 'move_url':
            arg = parsed['ARG1'] if 'ARG1' in parsed else parsed['ARG2']
            self.arguments_list.append(arg)
        if self.need_arguments and len(self.arguments_list) == 0:
            raise ValueError("We need argument!")

    def make_selenium_code(self, selector_list, driver):
        """
        Convert the function into selenium code and return
        Input:
            selector_list: List of dict(path, location. tagID)
        Output:
            func: seleninum function
            args: argument for 'func'
        """
        func, args = None, None

        element_id = self.find_target_element_for_selenium_with_nametuple(selector_list) if self.target_name is not None else None
        argument = self.find_argument_for_selenium_with_nametuple() if len(self.arguments_list) != 0 else None

        self.code_string += '\n# {}\n'.format(self.raw_clause)
        if self.func_name == 'click':
            if self.run_selenium: func = driver.find_element_by_css_selector(element_id).click
            self.code_string += 'try:\n    driver.find_element_by_css_selector("{}").click()\nexcept:\n    driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector("{}"))'.format(element_id, element_id)

        elif self.func_name == 'wait':
            if self.run_selenium: func = time.sleep
            args = argument
            self.code_string += 'import time\ntime.sleep({})'.format(args)
        elif self.func_name == 'write':
            if self.run_selenium: func = driver.find_element_by_css_selector(element_id).send_keys
            args = argument
            self.code_string += "driver.find_element_by_css_selector('{}').send_keys('{}')".format(element_id, args)
        elif self.func_name == 'contain_value':
            if self.run_selenium: func = argument in driver.page_source
            arg = argument
            self.code_string += 'assert "{}" in driver.page_source'.format(arg)
        elif self.func_name == 'refresh':
            if self.run_selenium: func = driver.refresh
            self.code_string += 'driver.refresh()'
        elif self.func_name == 'move_url':
            if self.run_selenium: func = driver.get
            args = argument
            self.code_string += "driver.get('{}')".format(args)
        self.selenium_func = func
        self.selenium_argument = args

    def run_selenium_code(self):
        if self.selenium_argument is not None:
            self.selenium_func(self.selenium_argument)
        else:
            self.selenium_func()

    def find_argument_for_selenium_with_nametuple(self):
        if self.arguments_list[0].count('"') == 1: self.arguments_list[0] += '"'
        assert self.arguments_list[0].count('"') in [0, 2]
        assert len(self.arguments_list) == 1
        argument = self.arguments_list[0]

        if '"' in argument:
            start_idx = argument.index('"') + 1
            end_idx = start_idx + argument[start_idx:].index('"')
            argument_token = argument[start_idx:end_idx].strip()

            if 'sec' in argument or 'second' in argument or 'min' in argument or 'minute' in argument:
                tok = ''
                for el in argument:
                    if el in '0123456789':
                        tok += el
                argument_token = int(tok)
                if 'min' in argument or 'minute' in argument:
                    argument_token *= 60
            return argument_token
        try:
            assert self.func_name == 'refresh'
        except:
            print(argument)
            return argument
        return

    def find_target_element_for_selenium_with_nametuple(self, selector_list):
        assert self.target_name is not None and '#' in self.target_name

        element = None
        for idx,tok in enumerate(self.target_name.split()):
            if tok == '#':
                assert idx < len(self.target_name.split()) - 1
                element = int(self.target_name.split()[idx + 1])


        if element is None: raise ValueError

        selector_path = None
        for selector in selector_list:
            if element == selector['tagId']:
                selector_path = selector['path']

        return selector_path

        # start_idx = self.target_name.index('"') + 1
        # end_idx = start_idx + self.target_name[start_idx:].index('"')
        # target_token = self.target_name[start_idx:end_idx].strip()
        #
        # name_tuple = {k:v for (k,v) in name_tuple}
        # assert target_token in name_tuple
        #
        # target_id = name_tuple[target_token]
        # return target_id

class EmbedManager:
    def __init__(self):
        self.keyman = KeywordManager()
        self.save_path = './dat/emb_dump.pck'
        self.embed_path = './dat/glove.6B.200d.txt'
        self.keyword_vector = dict()
        self.matrix = dict()
        self.get_vector_and_word()

    def get_vector_and_word(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, 'rb') as f:
                self.keyword_vector, self.matrix = pickle.load(f)
        else:
            self.keyword_vector, self.matrix = self.save_keyword_vector_and_word_list()

    def save_keyword_vector_and_word_list(self):
        """ Save the vector of keyword """
        keyword_vector = dict()
        mat = self.get_word_matrix(self.embed_path)
        self.matrix = mat
        for func_name in self.keyman.func2keyword:
            keyword_vector[func_name] = self.keyman.func2keyword[func_name]
        keyword_vector = self.get_func_name_vector_representation(keyword_vector)
        with open(self.save_path, 'wb') as f:
            pickle.dump([keyword_vector, mat], f)
        return keyword_vector, mat

    def get_func_by_emb(self, word):
        """
        When keyword of input natural language is not specified, use word embedding similarity to decide.
        Input:
            word(str): verb word of natural language
        Output
            tuple of (func_name(str), similarity score(float))
        """
        word_vector = self.matrix[word]
        word_vector = word_vector/np.linalg.norm(word_vector)
        sim_dict = {}
        for func_name in self.keyword_vector:
            sim = self.cosine_similarity(self.keyword_vector[func_name], word_vector)
            sim_dict[func_name] = sim
        #sorted_sim = sorted(sim_dict.items(), key=operator.itemgetter(1), reverse=True)
        return sim_dict

    def get_func_name_vector_representation(self, keyword_vector):
        """
        Make each keyword into vector for further.
        Input:
            keyword_vector(dict[func_name: [keyword1, keyword2..]):
        Output:
            keyword_vector(dict[func_name: average of each keyword vector])
        """
        vector_map = dict()
        for func_name in keyword_vector:
            keyword_list = keyword_vector[func_name]
            vectors = np.asarray([self.matrix[keyword] for keyword in keyword_list])
            vector = np.mean(vectors, axis=0)
            vector = vector/np.linalg.norm(vector)
            vector_map[func_name] = vector
        return vector_map

    @staticmethod
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @staticmethod
    def get_word_matrix(glove_path):
        """ Load word embedding matrix """
        map = dict()
        with open(glove_path, 'r', encoding='utf8') as f:
            ls = f.readlines()
            for idx, line in enumerate(ls):
                if idx % 10000 == 0:
                    print("{}/{}".format(idx, len(ls)))
                line = line.strip().split()
                try:
                    assert len(line) == 201  # word embedding vector length + word
                except:
                    continue
                vec = np.array([float(el) for el in line[1:]], dtype=np.float32)
                map[line[0]] = vec
        return map
