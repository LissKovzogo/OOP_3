class A:
    def go(self):
        print("Go, A!")
class B(A):
    def go(self, name):
        print('Go, {}!'.format(name))