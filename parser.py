#!/usr/bin/env python

from lexer import Tokenizer
import sys

# Rule type
TERMINAL = 0
RULE = 1

# Terminals
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
WHILESTATEMENT = 12
FORSTATEMENT = 13
CALLSTATEMENT = 14
CALL = 15
PARAMETERS = 16
MULTIPARAMETERS = 17
PARAMETER = 18
FACTOR = 19
LITERAL = 20
TERM = 21
MULTIFACTOR = 22
ADDITION = 23
MULTITERM = 24
RELATION = 25
MULTIADDITION = 26
EQUALITY = 27
MULTIRELATION = 28
CONJUNCTION = 29
MULTIEQUALITY = 30
EXPRESSION = 31
MULTICONJUNCTION = 32
ARGUMENTS = 33
MULTIEXPRESSION = 34
ASSIGNMENT = 35
CALLORASSIGNMENT = 36
INDEXDECLARATION = 37
DECLORASSIGNMENT = 38
RETURNSTATEMENT = 39
RETURNEXPRESSION = 40
TYPEOREMPTY = 41
MULTINOTMAIN = 42
IDORCALL = 43

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
    WHILESTATEMENT: "WHILESTATEMENT",
    FORSTATEMENT: "FORSTATEMENT",
    CALLSTATEMENT: "CALLSTATEMENT",
    CALL: "CALL",
    PARAMETERS: "PARAMETERS",
    MULTIPARAMETERS: "MULTIPARAMETERS",
    PARAMETER: "PARAMETER",
    FACTOR: "FACTOR",
    LITERAL: "LITERAL",
    TERM: "TERM",
    MULTIFACTOR: "MULTIFACTOR",
    ADDITION: "ADDITION",
    MULTITERM: "MULTITERM",
    RELATION: "RELATION",
    MULTIADDITION: "MULTIADDITION",
    EQUALITY: "EQUALITY",
    MULTIRELATION: "MULTIRELATION",
    CONJUNCTION: "CONJUNCTION",
    MULTIEQUALITY: "MULTIEQUALITY",
    EXPRESSION: "EXPRESSION",
    MULTICONJUNCTION: "MULTICONJUNCTION",
    ARGUMENTS: "ARGUMENTS",
    MULTIEXPRESSION: "MULTIEXPRESSION",
    ASSIGNMENT: "ASSIGNMENT",
    CALLORASSIGNMENT: "CALLORASSIGNMENT",
    INDEXDECLARATION: "INDEXDECLARATION",
    DECLORASSIGNMENT: "DECLORASSIGNMENT",
    RETURNSTATEMENT: "RETURNSTATEMENT",
    RETURNEXPRESSION: "RETURNEXPRESSION",
    TYPEOREMPTY: "TYPEOREMPTY",
    MULTINOTMAIN: "MULTINOTMAIN",
    IDORCALL: "IDORCALL",
    -1: "UNDEFINED"

}

class Parser():

    def __init__(self, tokenizer):

        self.rules = [
            [(RULE, NOTMAIN), (RULE, MULTINOTMAIN), (RULE, MAIN)], #0
            [(RULE, MAIN)],
            [(TERMINAL, KWMAIN), (TERMINAL, PARST), (TERMINAL, PAREND), (TERMINAL, CLBRST), (RULE, DECLARATIONS), (TERMINAL, CLBREND)],
            [(RULE, TYPEOREMPTY), (TERMINAL, ID), (RULE, FUNCTIONORGLOBAL)],
            [(TERMINAL, PARST), (RULE, PARAMETERS), (TERMINAL, PAREND), (TERMINAL, CLBRST), (RULE, DECLARATIONS), (TERMINAL, CLBREND)],
            [(RULE, GLOBAL)], #5
            [(TERMINAL, ST)],
            [(TERMINAL, ITYPE), (RULE, ARRAY)],
            [(TERMINAL, BTYPE), (RULE, ARRAY)],
            [(TERMINAL, FTYPE), (RULE, ARRAY)],
            [(TERMINAL, STRTYPE), (RULE, ARRAY)],  # 10
            [(RULE, TYPE), (TERMINAL, ID), (RULE, ARRAY), (RULE, DECLORASSIGNMENT), (TERMINAL, ST), (RULE, DECLARATIONS)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, SQBRST), (RULE, INDEXDECLARATION), (TERMINAL, SQBREND)],
            [(TERMINAL, EPSILON)],
            [(RULE, STATEMENTS)], #15
            [(TERMINAL, ST), (RULE, STATEMENTS)],
            [(RULE, IFSTATEMENT)],
            [(TERMINAL, KWIF), (TERMINAL, PARST), (RULE, EXPRESSION), (TERMINAL, PAREND), (RULE, STATEMENTS)],
            [(TERMINAL, EPSILON)],
            [(RULE, ELSESTATEMENT), (RULE, STATEMENTS)], #20
            [(TERMINAL, KWELSE), (RULE, STATEMENTS)],
            [(TERMINAL, EPSILON)],
            [(RULE, BLOCK), (RULE, STATEMENTS)],
            [(TERMINAL, CLBRST), (RULE, STATEMENTS), (TERMINAL, CLBREND)],
            [(RULE, WHILESTATEMENT), (RULE, STATEMENTS)], #25
            [(TERMINAL, KWWHILE), (TERMINAL, PARST), (RULE, EXPRESSION), (TERMINAL, PAREND), (RULE, STATEMENTS)],
            [(RULE, FORSTATEMENT), (RULE, STATEMENTS)],
            [(TERMINAL, KWFOR), (TERMINAL, ID), (TERMINAL, OPMBR), (RULE, CALL), (RULE, STATEMENTS)],
            [(RULE, CALLSTATEMENT), (RULE, STATEMENTS)],
            [(RULE, CALL), (TERMINAL, ST)], #30
            [(TERMINAL, ID), (RULE, CALLORASSIGNMENT)],
            [(RULE, PARAMETER), (RULE, MULTIPARAMETERS)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, CLN), (RULE, PARAMETER)],
            [(TERMINAL, EPSILON)], #35
            [(RULE, TYPE), (TERMINAL, ID)],
            [(TERMINAL, ID), (RULE, IDORCALL)],
            [(RULE, LITERAL)],
            [(TERMINAL, CTEINT)],
            [(TERMINAL, LTBOOL)], #40
            [(TERMINAL, CTEFLOAT)],
            [(TERMINAL, LTSTRING)],
            [(RULE, FACTOR), (RULE, MULTIFACTOR)],
            [(TERMINAL, OPML), (RULE, FACTOR), (RULE, MULTIFACTOR)],
            [(TERMINAL, EPSILON)], #45
            [(RULE, TERM), (RULE, MULTITERM)],
            [(TERMINAL, OPAD), (RULE, TERM), (RULE, MULTITERM)],
            [(TERMINAL, EPSILON)],
            [(RULE, ADDITION), (RULE, MULTIADDITION)],
            [(TERMINAL, OPREL), (RULE, ADDITION), (RULE, MULTIADDITION)], #50
            [(TERMINAL, EPSILON)],
            [(RULE, RELATION), (RULE, MULTIRELATION)],
            [(TERMINAL, OPEQ), (RULE, RELATION), (RULE, MULTIRELATION)],
            [(TERMINAL, EPSILON)],
            [(RULE, EQUALITY), (RULE, MULTIEQUALITY)], #55
            [(TERMINAL, OPCONJ), (RULE, EQUALITY), (RULE, MULTIEQUALITY)],
            [(TERMINAL, EPSILON)],
            [(RULE, CONJUNCTION), (RULE, MULTICONJUNCTION)],
            [(TERMINAL, OPDISJ), (RULE, CONJUNCTION), (RULE, MULTICONJUNCTION)],
            [(TERMINAL, EPSILON)], #60
            [(RULE, EXPRESSION), (RULE, MULTIEXPRESSION)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, CLN), (RULE, EXPRESSION), (RULE, MULTIEXPRESSION)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, KWPRINT),  (TERMINAL, PARST), (RULE, ARGUMENTS), (TERMINAL, PAREND)], #65
            [(RULE, ARRAY), (TERMINAL, OPAT), (RULE, EXPRESSION)],
            [(TERMINAL, PARST), (RULE, ARGUMENTS), (TERMINAL, PAREND)],
            [(RULE, ASSIGNMENT)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, EPSILON)], #70
            [(RULE, ASSIGNMENT)],
            [(TERMINAL, EPSILON)],
            [(TERMINAL, KWRANGE), (TERMINAL, PARST), (RULE, ARGUMENTS), (TERMINAL, PAREND)],
            [(RULE, EXPRESSION)],
            [(TERMINAL, PARST), (RULE, EXPRESSION), (TERMINAL, PAREND)],    #75
            [(RULE, RETURNEXPRESSION), (TERMINAL, ST)],
            [(TERMINAL, KWRETURN), (RULE, EXPRESSION)],
            [(RULE, RETURNSTATEMENT), (RULE, STATEMENTS)],
            [(RULE, TYPE)],
            [(TERMINAL, EPSILON)], #80
            [(RULE, NOTMAIN), (RULE, MULTINOTMAIN)],
            [(TERMINAL, EPSILON)],
            [(RULE, ARRAY)],
            [(TERMINAL, PARST), (RULE, ARGUMENTS), (TERMINAL, PAREND)],
            [(TERMINAL, KWINPUT), (TERMINAL, PARST), (RULE, ARGUMENTS), (TERMINAL, PAREND)], #85
            # []
        ]

        self.table = [
            [1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1],
            [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 3, 3, 3, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 5, -1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 10, 7, 9, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 15, 15, -1, 15, 15, -1, 11, 11, 11, 11, -1, -1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, 15, -1, -1, -1, 15, -1, -1, 12, -1, -1, 15, -1, 12],
            [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 14, 14, 14, 14, 14, 14, 14, -1, 14],
            [-1, -1, 29, 17, 20, 27, 25, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 16, -1, -1, -1, 23, -1, -1, 19, -1, 78, 29, -1, 19],
            [-1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 22],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 30, -1, -1],
            [-1, -1, 65, -1, -1, -1, -1, 73, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 32, 32, 32, 32, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33, -1, -1, -1, -1, -1, -1, 33],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34, -1, -1, -1, 35, -1, -1, -1, -1, -1, -1, 35],
            [-1, -1, -1, -1, -1, -1, -1, -1, 36, 36, 36, 36, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 85, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, 38, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 75, -1, -1, -1, -1, -1, 38, -1, 37, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, 39, 40, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1],
            [-1, 43, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 43, 43, 43, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 43, -1, -1, -1, -1, -1, 43, -1, 43, -1, -1],
            [-1, -1, -1, -1, -1, -1, 45, -1, -1, -1, -1, -1, -1, 45, -1, 45, 45, -1, -1, 45, 44, 45, 45, -1, 45, 45, -1, 45, -1, 45, 45, -1, -1, -1, -1, -1, 45],
            [-1, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 46, 46, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 46, -1, -1, -1, -1, -1, 46, -1, 46, -1, -1],
            [-1, -1, -1, -1, -1, -1, 48, -1, -1, -1, -1, -1, -1, -1, -1, 48, 48, -1, -1, 47, -1, 48, 48, -1, 48, 48, -1, 48, -1, 48, 48, -1, -1, -1, -1, -1, 48],
            [-1, 49, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 49, 49, 49, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 49, -1, -1, -1, -1, -1, 49, -1, 49, -1, -1],
            [-1, -1, -1, -1, -1, -1, 51, -1, -1, -1, -1, -1, -1, -1, -1, 50, 51, -1, -1, -1, -1, 51, 51, -1, 51, 51, -1, 51, -1, 51, 51, -1, -1, -1, -1, -1, 51],
            [-1, 52, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 52, 52, 52, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 52, -1, -1, -1, -1, -1, 52, -1, 52, -1, -1],
            [-1, -1, -1, -1, -1, -1, 54, -1, -1, -1, -1, -1, -1, -1, -1, -1, 53, -1, -1, -1, -1, 54, 54, -1, 54, 54, -1, 54, -1, 54, 54, -1, -1, -1, -1, -1, 54],
            [-1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, 55, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1, 55, -1, 55, -1, -1],
            [-1, -1, -1, -1, -1, -1, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 56, 57, -1, 57, 57, -1, 57, -1, 57, 57, -1, -1, -1, -1, -1, 57],
            [-1, 58, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 58, 58, 58, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 58, -1, -1, -1, -1, -1, 58, -1, 58, -1, -1],
            [-1, -1, -1, -1, -1, -1, 60, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 59, -1, 60, 60, -1, 60, -1, 60, 60, -1, -1, -1, -1, -1, 60],
            [-1, 61, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 61, 61, 61, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, 61, -1, 61, -1, 62],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 63, -1, 64, -1, 64, 64, -1, -1, -1, -1, -1, 64],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 66, -1, -1, -1, -1, -1, -1, -1, -1, -1, 66, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 68, -1, -1, -1, -1, -1, -1, -1, -1, 67, 68, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 74, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 70, -1, -1, -1, 74, -1, 70],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 71, -1, -1, -1, -1, -1, -1, 72, -1, -1, 71, -1, -1, -1, -1, -1, -1, -1, -1, 72],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 76, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 77, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 79, 79, 79, 79, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 80, -1, 80],
            [82, -1, -1, -1, -1, -1, -1, -1, 81, 81, 81, 81, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 81, -1, 82],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, 14, 14, 14, 14, 14, 14, 14, -1, 14, 14, 84, 83, -1, 14, 14, -1, -1, -1, -1, -1, -1]
        ]

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

    def get_production_stack(self, stack=None):
        result = []
        if(stack == None):
            stack = self.stack
        for item in stack:
            if(item[0] == TERMINAL):
                categories = self.tokens.categories
                key = list(categories.keys())[list(categories.values()).index(item[1])]
                result.append(key)
            else:
                result.append(toRuleString[item[1]])

        return " ".join(result)


    def execution_summary(self, token=None):
        """ For debug purposes """

        print("STACK:")
        self.printStack()

        print("Token: ")
        print(token)

        print("Last transition: ", self.last_transition)

    def rule_to_str(self, t):
        """ Converts terminals and non-terminals to a string represntation """

        if(t[0] == TERMINAL):
            return self.terminal_to_str(t[1])
        else:
            return toRuleString[t[1]]

    def print_production(self, transition_index, value):
        """ Prints the production visualization """

        transition = self.rules[transition_index]
        str_list = [self.rule_to_str(t) for t in transition]
        print("          (%04d, %10s) {%s}" % (transition_index, toRuleString[value], " ".join(str_list)))

    def parse(self):
        """ Parse the contents of the input following the rules of the grammar
            and the parse table.

            In each iteration the parser will check if the top of the stack is a
            terminal and see if it matches the token. If it is a non-terminal (RULE),
            a corresponding production (decided by checking the parse table) will be
            pushed to the stack.
        """
        readnext = False
        error = False
        errorInfo = (-100, -100)
        token = self.tokens.nextToken()
        accepted = False
        while len(self.stack) > 0:
            (type, value) = self.stack.pop()
            self.runtime_transitions.append((type, value))

            if(readnext):
                token = self.tokens.nextToken()

            if (type == TERMINAL):
                if (value == token.category_num or value == EPSILON):
                    if(value != EPSILON):
                        print(token)

                    if (not self.tokens.hasToken() and len(self.stack) == 0):
                        print("Input Accepted!")
                        error = False
                        accepted = True

                    if(value != EPSILON):
                        readnext = True

                else:
                    error = True
                    errorInfo = (value, token.category_num)



            elif (type == RULE):
                if(token.category_num > -1):
                    rule = self.table[value][token.category_num]

                    self.print_production(rule, value)
                    self.last_transition = rule

                    if(rule == -1):
                        print(toRuleString[value], self.terminal_to_str(token.category_num))
                        break
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
