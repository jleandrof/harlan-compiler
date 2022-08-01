from lexer import Tokenizer
import sys

# Rule type
TERMINAL = 0
RULE = 1

# Terminals
# KWMAIN = 0
# PARST = 1
# PAREND = 2
# CLBRST = 3
# CLBREND = 4
# ITYPE = 5
# ID = 6
# ST = 7

KWMAIN = 0
KWINPUT = 1
KWPRINT = 2
KWIF = 3
KWELSE = 4
KWFOR = 5
KWWHILE = 6
KWRANGE = 7
STRTYPE = 8
ITYPE = 9
FTYPE = 10
BTYPE = 11
CTEFLOAT = 12
CTEINT = 13
LTBOOL = 14
OPREL = 15
OPEQ = 16
OPAT = 17
OPMBR = 18
OPAD = 19
OPML = 20
OPCONJ = 21
OPDISJ = 22
OPNEG = 23
ST = 24
CLN = 25
PARST = 26
SQBRST = 27
CLBRST = 28
PAREND = 29
SQBREND = 30
CLBREND = 31
LTSTRING = 32
KWRETURN = 33
ID = 34
INVALID = 35

EPSILON = 36

# Non-Terminals
# PROGRAM = 0
# MAIN = 1
# FUNCTIONORGLOBAL = 2
# GLOBAL = 3
# PARAMETERS = 4
# PARAMETER = 5
# DECLARATIONS = 6
# DECLARATION = 7
# TYPE = 8
# TYPEOREMPTY = 9
# STATEMENTS = 10
# STATEMENT = 11
# BLOCK = 12
# ASSIGNMENT = 13
# IFSTATEMENT = 14
# WHILESTATEMENT = 15
# FORSTATEMENT = 16
# EXPRESSION = 17
# CONJUNCTION = 18
# EQUALITY = 19
# EQUOP = 20
# RELATION = 21
# RELOP = 22
# ADDITION = 23
# ADDOP = 24
# TERM = 25
# MULOP = 26
# FACTOR = 27
# IDENTIFIER = 28
# LETTER = 29
# DIGIT = 30
# LITERAL = 31
# INTEGER = 32
# BOOLEAN = 33
# FLOAT = 34
# STRING = 35
# ASCIICHAR = 36
# CALLSTATEMENT = 37
# RETURNSTATEMENT = 38
# RETURNEXPRESSION = 39
# CALL = 40
# ARGUMENTS = 41
PROGRAM = 0
MAIN = 1
NOTMAIN = 2
FUNCTIONORGLOBAL = 3
GLOBAL = 4
TYPE = 5
DECLARATIONS = 6
ARRAY = 7
STATEMENTS = 8
IFSTATEMENT = 9
ELSESTATEMENT = 10
BLOCK = 11


toRuleString = {
    PROGRAM: "PROGRAM",
    MAIN: "MAIN",
    NOTMAIN: "NOTMAIN",
    FUNCTIONORGLOBAL: "FUNCTIONORGLOBAL",
    GLOBAL: "GLOBAL",
    TYPE: "TYPE",
    DECLARATIONS: "DECLARATIONS",
    ARRAY: "ARRAY",
    STATEMENTS: "STATEMENTS",
    IFSTATEMENT: "IFSTATEMENT",
    ELSESTATEMENT: "ELSESTATEMENT",
    BLOCK: "BLOCK",
    -1: "UNDEFINED"

}

toCategoryNum = {
    0: 1,
    1: 27,
    2: 30,
    3: 29,
    4: 32,
    5: 10,
    6: 35,
    7: 25
}

toEnum = {

    1: 0,
    27: 1,
    30: 2,
    29: 3,
    32: 4,
    10: 5,
    35: 6,
    25: 7,
    -1: -1
}

class Parser():

    def __init__(self, tokenizer):

        self.rules = [
            [(RULE, NOTMAIN), (RULE, MAIN)],
            [(RULE, MAIN)],
            [(TERMINAL, KWMAIN), (TERMINAL, PARST), (TERMINAL, PAREND), (TERMINAL, CLBRST), (RULE, DECLARATIONS), (TERMINAL, CLBREND)],
            [(RULE, TYPE), (TERMINAL, ID), (RULE, FUNCTIONORGLOBAL), (RULE, NOTMAIN)],
            [(TERMINAL, PARST), (TERMINAL, PAREND), (TERMINAL, CLBRST), (RULE, DECLARATIONS), (TERMINAL, CLBREND)],
            [(RULE, GLOBAL)],
            [(TERMINAL, ST)],
            [(TERMINAL, ITYPE)],
            [(TERMINAL, BTYPE)],
            [(TERMINAL, FTYPE)],
            [(TERMINAL, STRTYPE)],  # 10
            [(RULE, TYPE), (RULE, ARRAY), (TERMINAL, ID), (RULE, ARRAY), (TERMINAL, ST), (RULE, DECLARATIONS)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, SQBRST), (TERMINAL, CTEINT), (TERMINAL, SQBREND)],
            [(TERMINAL, EPSILON)],
            [(RULE, STATEMENTS)], #15
            [(TERMINAL, ST), (RULE, STATEMENTS)],
            [(RULE, IFSTATEMENT)],
            [(TERMINAL, KWIF), (TERMINAL, PARST), (TERMINAL, PAREND), (RULE, STATEMENTS)],
            [(TERMINAL, EPSILON)],
            [(RULE, ELSESTATEMENT), (RULE, STATEMENTS)], #20
            [(TERMINAL, KWELSE), (RULE, STATEMENTS)],
            [(TERMINAL, EPSILON)],
            [(RULE, BLOCK), (RULE, STATEMENTS)],
            [(TERMINAL, CLBRST), (RULE, STATEMENTS), (TERMINAL, CLBREND)],

            [(TERMINAL, EPSILON)]   # Epsilon at the end seems to make it kinda work


            # [(TERMINAL, CLBRST), (RULE, STATEMENTS), (TERMINAL, CLBREND)],
            # [(RULE, BLOCK), (RULE, STATEMENTS)],


            # [(TERMINAL, ST)], # 15
            # [(RULE, IFSTATEMENT)],
            # [],
            # [(TERMINAL, KWIF), (TERMINAL, PARST), (TERMINAL, PAREND), (RULE, STATEMENTS)],
            # [(TERMINAL, KWELSE), (RULE, STATEMENTS)],
            # []
        ]



        # self.table = [[1, -1, -1, -1, -1, -1, -1, -1], [2, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, 3, -1, -1]]
        # self.table = [[0, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1],
        #  [1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, 4, 4, 4, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, 5, 5, 5, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, 6, 6, 6, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, 7, 7, 7, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        #  [-1, -1, -1, -1, -1, -1, -1, -1, 8, 8, 8, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, 9, 9, 9, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, 10, -1, 10, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, 10, -1, -1, -1, -1, 10, 10, -1], [-1, -1, -1, 11, -1, 11, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1, 11, -1, -1, -1, -1, 11, 11, -1], [-1, -1, -1, 12, -1, 12, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, 12, -1, -1, -1, -1, 12, 12, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1], [-1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, 17, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, 17, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, 18, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18, -1, 18, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, 19, 19, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, -1, 19, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, 21, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 21, -1, 21, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, 23, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, -1, 23, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25, 25, 25, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25, -1, 25, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, 27, 27, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, -1, 27, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 28, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 29, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, 31, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 35, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 39, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 40, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, 41, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, -1, -1, -1, -1, -1, 41, -1, 41, -1]]
        self.table = [[1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, 3, 3, 3, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, 10, 7, 9, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, 15, -1, -1, -1, -1, 11, 11, 11, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, 12], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, 14], [-1, -1, -1, 17, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, 23, -1, -1, 19, -1, -1, -1, -1, 19], [-1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1]]


        self.stack = [(RULE, PROGRAM)]
        self.tokens = tokenizer
        self.runtime_transitions = []
        self.last_transition = -1

    def terminal_to_str(self, code):
        categories = self.tokens.categories
        return list(categories.keys())[list(categories.values()).index(code)]

    def print_transitions(self):
        self.printStack(self.runtime_transitions)

    def printStack(self, stack=None):
        result = []
        if(stack == None):
            stack = self.stack
        for item in stack:
            if(item[0] == 0):
                categories = self.tokens.categories
                key = list(categories.keys())[list(categories.values()).index(item[1])]
                result.append(("TERMINAL", key))
            else:
                result.append(("RULE", toRuleString[item[1]]))

        print(result)

    def execution_summary(self, token=None):
        print("STACK:")
        self.printStack()

        # print("Runtime Transitions:")
        # self.print_transitions()

        print("Token: ")
        print(token)

        print("Last transition: ", self.last_transition)


    def parse(self):
        readnext = False
        error = False
        errorInfo = (-100, -100)
        token = self.tokens.nextToken()
        accepted = False
        while len(self.stack) > 0:
            # self.execution_summary(token)
            # input()
            (type, value) = self.stack.pop()
            self.runtime_transitions.append((type, value))

            if(readnext):
                token = self.tokens.nextToken()

            if (type == TERMINAL):
                if (value == token.category_num or value == EPSILON):
                    print(token)
                    if (not self.tokens.hasToken() and len(self.stack) == 0):
                        print("input accepted")
                        error = False
                        accepted = True

                    if(value != EPSILON):
                        readnext = True

                else:
                    print("erro aqui")
                    error = True
                    errorInfo = (value, token.category_num)



            elif (type == RULE):
                if(token.category_num > -1):
                    rule = self.table[value][token.category_num]
                    # print(toRuleString[value], self.terminal_to_str(token.category_num))
                    # print(self.stack)
                    # print(list(reversed(self.rules[rule])))
                    self.last_transition = rule
                    for r in reversed(self.rules[rule]):
                        self.stack.append(r)


                    readnext = False

            if(error):
                break;

        if(error):
            print("Syntax error on position (%d, %d): [%s] expected. Got [%s]" % (token.line, token.column, self.terminal_to_str(errorInfo[0]), self.terminal_to_str(errorInfo[1])))
            print(token)
            self.printStack()

if(__name__ == "__main__"):

    for filename in sys.argv[1:]:
        print(filename + ":")
        with open(filename) as f:
            target = f.read()
            tokenizer = Tokenizer(target)

            parser = Parser(tokenizer)
            parser.parse()

            print()
