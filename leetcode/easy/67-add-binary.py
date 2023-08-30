"""
I can't tell if this is a great solution or a terrible solution.  I split each
string into a list, then recurse with a carried integer variable, then slap it
all back together as a string at the end.
"""

class Solution:
    def addBinary(self, a: str, b: str) -> str:
        """
        :type a: str
        :type b: str
        :rtype: str
        """            
        o = str()
        c = 0
        a = list(a)
        b = list(b)
        def adder(l1:list, l2:list, carry:int): 
            out = []
            if not any([l1, l2, carry]):
                return out
            if l1:
                a = int(l1.pop())
            else:
                a = 0
            if l2:
                b = int(l2.pop())
            else:
                b = 0
            x = a + b + carry
            y = x % 2
            carry = x // 2
            out += adder(l1, l2, carry)
            out.append(y)
            return out
        for i in adder(a, b, c):
            o += str(i)
        return o