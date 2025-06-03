import swizzle

@swizzle
class Test:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

class Test2(Test):
    z = 3
    def __init__(self):
        super().__init__()
class Test3:
    a = 3

if __name__=="__main__":
    test = Test()
    print(test.abc)
    print(test.cba[0:2])
    print(test.abc[0])
