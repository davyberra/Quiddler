class Test:
    def __init__(self):
        self.a = 1
        self.b = 2

    def call(self):
        self.b = 4


class Parent:
    def __init__(self):
        self.tests = []

    def add(self, t: Test):
        self.tests.append(t)
p = Parent()
t = Test()
p.add(t)
for test in p.tests:
    print(f'a: {test.a}, b: {test.b}')

t.call()
for test in p.tests:
    print(f'a: {test.a}, b: {test.b}')