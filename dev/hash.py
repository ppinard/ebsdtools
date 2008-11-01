

class foo:
  def __init__(self, a, b, c, d):
    self.a = a
    self.b = b
    self.c = c
    self.d = d
  
  def __hash__(self):
    value1 = hash(self.a)
    value2 = hash(self.b) * 10**len(str(value1))
    value3 = hash(self.c) * 10**(len(str(value1))+len(str(value2)))
    value4 = hash(self.d) * 10**(len(str(value1))+len(str(value2))+len(str(value3)))
    
    return value1+value2+value3+value4

if __name__ == '__main__':
  foo1 = foo(0.2, 0.3, 2, 1)
  foo2 = foo(-0.5e-10, 10, -7, 0.1)
  
  print hash(0.1)
  print foo2.__hash__()
  
  adict = {}
  
  adict.setdefault(foo1, 9)
  adict[foo1] = 1
  adict[foo2] = 8
  
  print adict