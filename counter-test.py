class Counter():

    def __init__(self, matrix):
        self.row = 0
        self.column = 0
        #self.counter = [(index, row) for index, row in enumerate(enumerate(matrix))]

    def __add__(self, other):
        
        if (self.column + 1) > len(matrix[self.row]):
            self.row += 1
            self.column = 0
        else:
            self.column += 1
#
        return self

    def __str__(self):

        return str((self.row, self.column))

matrix = ['this', 'is', 'a', 'matrix']

c = Counter(matrix)

print (c + 5)
