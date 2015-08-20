class Monad:
    def __init__(self, v):
        self.v = v
    def bind(self, f):
        return f(self, self.v)
    def unit(self, v):
        return self.__class__(v)


def action1(m): return m.unit(1)
def action2(m): return m.unit(2)
def action3(m, x,y): return m.unit(x+y)

m = Monad(None)
def _1(m1, x1):
    def _2(m2, x2):
        return action3(m2, x1, x2)
    return action2(m1).bind(_2)
lastline = action1(m).bind(_1)
print(lastline.v)
