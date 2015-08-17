class Monad:
    def __init__(self, f_or_v):
        if isinstance(f_or_v, Monad):
            f_or_v = f_or_v.f_or_v
        self.f_or_v = f_or_v
    def bind(self, f):
        return self.unit(f(self, self.f_or_v))
    def unit(self, f_or_v):
        return self.__class__(f_or_v)


def action1(m) -> Monad: return m.unit(1)
def action2(m) -> Monad: return m.unit(2)
def action3(m, x,y) -> Monad: return m.unit(x+y)

def r(f): return f.__annotations__['return']

m = Monad(None)
def _1(m1, x1):
    def _2(m2, x2):
        return action3(m2, x1, x2)
    return action2(m1).bind(_2)
lastline = action1(m).bind(_1)
print(lastline.f_or_v)
