import re
import sys

class Token():

    def __init__(self, pos, category, value):
        self.category_num, self.category_id = category
        self.value = value
        self.line, self.column = pos

    def __str__(self):
        return '[%03d, %03d] (%04d, %10s) {%s}' % (self.line, self.column, self.category_num, self.category_id, self.value)


class Tokenizer():

    def __init__(self, tokens, categories, target):
        
        self.tokens = tokens
        self.categories = categories
        self.column = 0
        self.row = 0
        self.regex = re.compile('|'.join('(?P<%s>%s)' % token for token in tokens))
        
        target = re.sub(re.compile('^.*\/\/.*?\n'), '', target)[:-1]
        #self.target = target.splitlines()
        self.target = [s for s in target.splitlines() if s]
        self.ws_skip = re.compile('\s+')

        #print(self.target)
        
    def hasToken(self):
        return False if (self.row >= len(self.target)) else True
        
    def nextToken(self):

        ws = self.ws_skip.match(self.target[self.row], self.column)
        if ws:
            self.column = ws.end()
            
        m = self.regex.match(self.target[self.row], self.column)
        if m:
            category_id = m.lastgroup
            category_num = self.categories[category_id]
            new_token = Token((self.row + 1, self.column + 1), (category_num, category_id), m.string[m.start():m.end()])
            self.column = m.end()
            if self.column >= len(self.target[self.row]):
                self.column = 0
                self.row += 1
            return new_token

        #print(self.target[self.row][self.column])
        self.column = len(self.target[self.row])
        self.row = len(self.target)
        return 'error'
        
if __name__ == '__main__':

    tokens = [
        ('KWMAIN', '(main)(?!\w)'),
        ('KWIO', '(input|print)(?!\w)'),
        ('KWIF', '(if)(?!\w)'),
        ('KWELSE', '(else)(?!\w)'),
        ('KWFOR', '(for)(?!\w)'),
        ('KWWHILE', '(while)(?!\w)'),
        ('KWRANGE', '(range)(?!\w)'),
        ('PTYPE', '(string|int|float|bool)(?!\w)'),
        ('CTEFLOAT', '[+-]?\d+\.\d+(?!\w)'),
        ('CTEINT', '[+-]?\d+(?!\w)'),
        ('LTBOOL', '(true|false)(?!\w)'),
        ('OPCMP', '>=|>|<=|<|==|!='),
        ('OPAT', '='),
        ('OPMBR', '(in)(?!\w)'),
        ('OPAD', '\+|-'),
        ('OPML', '\*|/|%'),
        ('OPCONJ', '(?<!\w)(and)(?!\w)'),
        ('OPDISJ', '(or)(?!\w)'),
        ('OPNEG', '(not)(?!\w)'),
        ('ST', ';'),
        ('CLN', ','),
        ('PARST', '\('),
        ('SQBRST', '\['),
        ('CLBRST', '\{'),
        ('PAREND', '\)'),
        ('SQBREND', '\]'),
        ('CLBREND', '\}'),
        ('STRING', '\".*?\"'),
        ('ID', '[a-zA-Z_]+[0-9]*[a-zA-Z_]*'),
    ]
    categories = {
        'KWMAIN': 1,
        'KWIO': 2,
        'KWIF': 3,
        'KWELSE': 4,
        'KWFOR': 5,
        'KWWHILE': 6,
        'KWRANGE': 7,
        'PTYPE': 8,
        'CTEFLOAT': 9,
        'CTEINT': 10,
        'LTBOOL': 11,
        'OPCMP': 12,
        'OPAT': 13,
        'OPMBR': 14,
        'OPAD': 15,
        'OPML': 16,
        'OPCONJ': 17,
        'OPDISJ': 18,
        'OPNEG': 19,
        'ST': 20,
        'CLN': 21,
        'PARST': 22,
        'SQBRST': 23,
        'CLBRST': 24,
        'PAREND': 25,
        'SQBREND': 26,
        'CLBREND': 27,
        'STRING': 28,
        'ID': 29
    }

    for filename in sys.argv[-1:]:
        print(filename + ":")
        with open(filename) as f:
            target = f.read()
            tokenizer = Tokenizer(tokens, categories, target)

            while tokenizer.hasToken():
                print(tokenizer.nextToken()) 
    
