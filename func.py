import time


class KeywordManager:
    def __init__(self):
        self.func2keyword = {
            'click':['click', 'touch'],
            'wait':['wait','sleep'],
            'write':['enter', 'put', 'write'],
            'contain_value':['have','has','contain'],
            'refresh':['refresh'],
            'move_url':['go','move']
        }
        self.keyword_list = [el for li in self.func2keyword.values() for el in li]
        assert len(self.keyword_list) == len(list(set(self.keyword_list)))
        self.keyword2func = {}
        for k,vlist in self.func2keyword.items():
            for v in vlist:
                self.keyword2func[v] = k  # reverse of func2keyword for each keyword


class Func:
    def __init__(self, clause, pos_tag_clause):
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
            verb_list.append(word)
            if word in self.keyman.keyword_list:
                if find_keyword:
                    raise ValueError("More than one keyword is exists, {} and {}".format(self.func_word, word))
                find_keyword = True
                self.func_word = word
                self.func_name = self.keyman.keyword2func[word]
                if self.func_name in ['write', 'wait']: self.need_arguments = True

        # Exact match with keyword is failed.
        if not find_keyword:
            # TODO: Use word embedding to match the function based on similarity.
            raise ValueError

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
            self.arguments_list.append(parsed['ARGM-TMP'])
        elif self.func_name == 'write':
            self.arguments_list.append(parsed['ARG1'])
        elif self.func_name == 'contain_value':
            pass
        elif self.func_name == 'refresh':
            self.arguments_list.append(parsed['ARG1'])
        elif self.func_name == 'move_url':
            self.arguments_list.append(parsed['ARG2'])

        if self.need_arguments and len(self.arguments_list) == 0:
            raise ValueError("We need argument!")

    def make_selenium_code(self, name_tuple, driver):
        """
        Convert the function into selenium code and return
        Input:
            name_tuple:
        Output:
            func: seleninum function
            args: argument for 'func'
        """
        func, args = None, None

        element_id = self.find_target_element_for_selenium_with_nametuple(name_tuple) if self.target_name is not None else None
        argument = self.find_argument_for_selenium_with_nametuple(name_tuple) if len(self.arguments_list) != 0 else None

        if self.func_name == 'click':
            element = driver.find_element_by_name(element_id)
            self.code_string += 'driver.find_element_by_name({})'.format(element_id)
            func = element.click
            self.code_string += '.click()'
        elif self.func_name == 'wait':
            func = time.sleep
            args = argument
            self.code_string = 'time.sleep({})'.format(args)
        elif self.func_name == 'write':
            element = driver.find_element_by_name(element_id)
            func = element.send_keys
            args = argument
            self.code_string = 'driver.find_element_by_name({}).send_keys({})'.format(element_id, args)
        elif self.func_name == 'contain_value':
            pass
        elif self.func_name == 'refresh':
            func = driver.refresh
            self.code_string = 'driver.refresh()'
        elif self.func_name == 'move_url':
            func = driver.get
            args = argument
            self.code_string = 'driver.get({})'.format(args)
        self.selenium_func = func
        self.selenium_argument = args

    def run_selenium_code(self):
        if self.selenium_argument is not None:
            self.selenium_func(self.selenium_argument)
        else:
            self.selenium_func()

    def find_argument_for_selenium_with_nametuple(self, name_tuple):
        if self.arguments_list[0].count('"') == 1: self.arguments_list[0] += '"'
        assert self.arguments_list[0].count('"') in [0, 2]
        assert len(self.arguments_list) == 1
        argument = self.arguments_list[0]

        if '"' in argument:
            start_idx = argument.index('"') + 1
            end_idx = start_idx + argument[start_idx:].index('"')
            argument_token = argument[start_idx:end_idx].strip()
            name_tuple = {k: v for (k, v) in name_tuple}
            if argument_token in name_tuple:
                argument_token = name_tuple[argument_token]

            if 'sec' in argument or 'second' in argument or 'min' in argument or 'minute' in argument:
                tok = ''
                for el in argument:
                    if el in '0123456789':
                        tok += el
                argument_token = int(tok)
                if 'min' in argument or 'minute' in argument:
                    argument_token *= 60
            return argument_token

        assert self.func_name == 'refresh'
        return

    def find_target_element_for_selenium_with_nametuple(self, name_tuple):
        assert self.target_name is not None and self.target_name.count('"') == 2

        start_idx = self.target_name.index('"') + 1
        end_idx = start_idx + self.target_name[start_idx:].index('"')
        target_token = self.target_name[start_idx:end_idx].strip()

        name_tuple = {k:v for (k,v) in name_tuple}
        assert target_token in name_tuple

        target_id = name_tuple[target_token]
        return target_id
