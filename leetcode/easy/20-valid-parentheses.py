"""
My solution here is to use a stack to track unmatched parens, and a dict to recall valid pairs.
"""

class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {'}':'{', ']':'[',')':'('}
        stack = list()
        
        for c in s:
            match c:
                case '[' | '{' | '(':
                    stack.append(c)
                case ']' | '}' | ')':
                    try:
                        if stack.pop() != pairs[c]:
                            return False
                    except:
                        return False

        if len(stack) == 0:
            return True
        else:
            return False