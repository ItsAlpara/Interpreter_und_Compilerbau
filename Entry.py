class Entry:
    def __init__(self):
        self.value = None

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def push(self, names):
        return SymbolTable(self).put(names)

    def put(self, names):
        for name in names:
            if name not in self.vars:
                self.vars[name] = Entry()
        return self

    def root(self):
        t = self
        while t.parent:
            t = t.parent
        return t

    def __contains__(self, name):
        if name in self.vars:
            return True
        elif self.parent is None:
            return False
        else:
            return name in self.parent

    def __getitem__(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent is None:
            raise KeyError(name)
        else:
            return self.parent[name]
