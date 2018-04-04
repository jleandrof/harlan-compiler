#!/usr/bin/env python
""" Lexical Analizer"""

import re
import sys


class Token():

    
    def __init__(self, pos, category, value):
        self.category_num, self.category_id = category
        self.value = value
        self.line, self.column = pos

    def __str__(self):
        return '[%03d, %03d] (%04d, %10s) {%s}' % (self.line,
                                                   self.column,
                                                   self.category_num,
                                                   self.category_id,
                                                   self.value)


class Tokenizer():
    """Separate a string into tokens

    Attributes:
        tokens (list of tuples): Each tuple stores a token category and 
            its regular expression.
        categories (dict): Maps the category names to its identification 
            numbers.
        column (int): Number of the current column.
        row (int): Number of the current row.
        regex (:obj:'re'): The regex from the tokens atribute grouped and
            joined by the '|' operator.
        target (list of str): The entire target string is passed on the 
            constructor. It will be stripped of comments and split into lines
        ws_skip (:obj:'re'): Regular expression to match whitespace.
    """

    
    def __init__(self, target):
#TODO:
#    Fix token specification
        self.tokens = [
            ('KWMAIN', '(main)(?!\w)'),
            ('KWIO', '(input|print)(?!\w)'),
            ('KWIF', '(if)(?!\w)'),
            ('KWELSE', '(else)(?!\w)'),
            ('KWFOR', '(for)(?!\w)'),
            ('KWWHILE', '(while)(?!\w)'),
            ('KWRANGE', '(range)(?!\w)'),
            ('STRTYPE', '(string)(?!\w)'),
            ('ITYPE', '(int)(?!\w)'),
            ('FTYPE', '(float)(?!\w)'),
            ('BTYPE', '(bool)(?!\w)'),
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
            ('LTSTRING', '\".*?\"'),
            ('KWRETURN', '(return)(?!\w)'),
            ('ID', '[a-zA-Z_]+[0-9]*[a-zA-Z_]*'),
        ]
        
        self.categories = {
            'KWMAIN': 1,
            'KWIO': 2,
            'KWIF': 3,
            'KWELSE': 4,
            'KWFOR': 5,
            'KWWHILE': 6,
            'KWRANGE': 7,
            'STRTYPE': 8,
            'ITYPE': 9,
            'FTYPE': 10,
            'BTYPE': 11,
            'CTEFLOAT': 12,
            'CTEINT': 13,
            'LTBOOL': 14,
            'OPCMP': 15,
            'OPAT': 16,
            'OPMBR': 17,
            'OPAD': 18,
            'OPML': 19,
            'OPCONJ': 20,
            'OPDISJ': 21,
            'OPNEG': 22,
            'ST': 23,
            'CLN': 24,
            'PARST': 25,
            'SQBRST': 26,
            'CLBRST': 27,
            'PAREND': 28,
            'SQBREND': 29,
            'CLBREND': 30,
            'LTSTRING': 31,
            'KWRETURN': 32,
            'ID': 33
        }
        
        self.column = 0
        self.row = 0
        
        self.regex = re.compile('|'.join('(?P<%s>%s)' % token for token in self.tokens))
        self.ws_skip = re.compile('\s+')
        
        self.target = target.splitlines()
        for i, item in enumerate(self.target):
            self.target[i] = re.sub(re.compile('(?m)^ *\/\/.*\n?'), '', item)
        
    def hasToken(self):
        """Check if there are tokens remaining in the string."""

        return False if self.row >= len(self.target) else True
        
    def nextToken(self):
        """Returns the next matched token.

        The first section checks if there are empty lines on the next
        position - If so, the current row will be updated to skip
        them. Whitespaces are skipped here by ws_skip.
        Returns 'Invalid token' if no token is matched.
        """

        while(self.hasToken() and not self.target[self.row]):
            self.row += 1
            
        if self.hasToken():
            ws = self.ws_skip.match(self.target[self.row], self.column) 
            if ws:
                self.column = ws.end()
            
            token_match = self.regex.match(self.target[self.row], self.column)
            if token_match:
                category_id = token_match.lastgroup
                category_num = self.categories[category_id]
                new_token = Token((self.row + 1, self.column + 1),
                                  (category_num, category_id),
                                  token_match.string[token_match.start():token_match.end()])
                self.column = token_match.end()
                if self.column >= len(self.target[self.row]):
                    self.column = 0
                    self.row += 1
                return new_token

            error = '[%03d, %03d] Invalid token' % (self.row + 1, self.column)
            self.row = len(self.target)
            return error
            
        return ''
    
