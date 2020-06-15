class a:
    def __init__(self, v):
        self.vv = v

class b:
    def __init__(self, v):
        self.vv = v

class c:
    def __init__(self):
        self.z = 0

c1 = c()

a1 = a(c1)

b1 = b(a1.vv)

print(a1.vv)
print(b1.vv)

a1.vv.z = 2
print(a1.vv.z)
print(b1.vv.z)