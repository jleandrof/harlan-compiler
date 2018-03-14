import re

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
        self.pos = 0
        
        self.regex = re.compile('|'.join('(?P<%s>%s)' % token for token in tokens))
        self.target = re.sub(re.compile('^.*\/\/.*?\n'), '', target)[:-1]
        self.ws_skip = re.compile('\s+')

    def hasToken(self):
        return False if self.pos >= len(self.target) else True
        
    def nextToken(self):
        
        ws = self.ws_skip.match(self.target, self.pos)
        if ws:
            self.pos = ws.end()
            
        m = self.regex.match(self.target, self.pos)
        if m:
            category_id = m.lastgroup
            category_num = self.categories[category_id]
            new_token = Token((self.pos, 1), (category_num, category_id), m.string[m.start():m.end()])
            self.pos = m.end()
            return new_token

        self.pos = len(self.target)
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
        'NEWLINE': 28,
        'ID': 29
    }

    with open('fib.hl') as f:
        target = f.read()
        target = target.split('\n')
        print(target)
        for line in target:
            tokenizer = Tokenizer(tokens, categories, line + '\n')

            while tokenizer.hasToken():
                print(tokenizer.nextToken()) 
    
