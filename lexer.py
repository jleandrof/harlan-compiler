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
        self.target = target
        self.tokens = tokens
        self.categories = categories
        print('|'.join('(P<%s>%s)' % token for token in tokens))
        self.regex = re.compile('|'.join('(?P<%s>%s)' % token for token in tokens))
        self.pos = 0

        self.ws_skip = re.compile('\S')

    def nextToken(self):
#TODO
# Decide if some of these are really necessary
        w = self.ws_skip.match(self.target, self.pos)
        if w:
            self.pos = w.start()
        else:
            return None
        
        m = self.regex.match(self.target, self.pos)

        if m:
            category_id = m.lastgroup
            category_num = self.categories[category_id]
            new_token = Token((self.pos, 1), (category_num, category_id), m.string)

            return new_token

        return 0
        
if __name__ == '__main__':

    tokens = [('id', '\w+')]
    categories = {'id': 1}

    tokenizer = Tokenizer(tokens, categories, '125')
    print(tokenizer.nextToken())
