class rgba():
    def __init__(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        print(self.to_normalized())
    
    def to_normalized(self):
        r_normalized = str(float(self.r / 255))[0:4]
        g_normalized = str(float(self.g / 255))[0:4]
        b_normalized = str(float(self.b / 255))[0:4]
        return r_normalized + ", " + g_normalized + ", " + b_normalized + ", " + str(self.a)

rgba(18, 0, 154, 0.8)