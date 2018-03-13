class Token(Object):

    def __init__(self, category, value, pos):
        self.category = category
        self.value = value
        self.pos = pos

    def __str__(self):
        return ''
