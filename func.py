
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
        self.keyword_list = [el for li in self.func2keyword for el in li]
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

    def assign_func_name(self):
        """
        Assign the function type by keyword matching with verb word in clause.
        If clause's verb doesn't exists in keyword, use w2v to find the most similar keyword and assign it.
        If there are more than one verb, how to deal with?
        Input:
            parser(StanfordCoreNLP object): to pos tag
        """

        # TODO: Implement the better way to find the " Verb". (e.g. parse the clause and select the main verb)
        find_keyword = False
        for (word,tag) in self.pos_tag_clause:
            if tag[0] != 'V': continue
            if word.lower() in [el for li in self.keyman.keyword_list for el in li]:
                if find_keyword:
                    raise ValueError("More than one keyword is exists, {} and {}".format(self.func_word, word))
                find_keyword = True
                self.func_word = word
                self.func_name = self.keyman.keyword2func[word]

    def make_selenium_code(self):
        """ Convert the function into selenium code and return """
        func, args = None, []
        return func, args


