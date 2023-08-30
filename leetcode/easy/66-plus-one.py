"""
This was a fun one. I was apparently not familiar with Pythons actual behavior
around reversing lists, so this was a good exercise.
"""

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        digits.reverse()
        carry = False
        for i,v in enumerate(digits):
            if digits[i] != 9:
                digits[i] += 1
                carry = False
                digits.reverse()
                return digits
            else:
                digits[i] = 0
                carry = True
        if carry:
            digits.append(1)
        digits.reverse()
        return digits