class XC:
    _counter = int(0)
    def __init__(self):
        XC._counter += 1
        self._id = XC._counter
    
    def get_id(self):
        return self._id

x1 = XC()
x2 = XC()
x3 = XC()
x4 = XC()
print(x1.get_id())
print(x1.get_id())
print(x3.get_id())
print(type(x4.get_id()))
