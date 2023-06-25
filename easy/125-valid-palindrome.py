"""
This solution munges then folds the string to check for palindromicity.
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        # preprocess string
        w = str()
        for c in s:
            if not c.isalnum():
                continue
            else: 
                w += c.lower()

        # check length
        mid = len(w) // 2
        count = 0

        # even case
        if len(w) % 2 == 0:
            while count < mid:
                if w[mid-1-count] != w[-mid+count]:
                    return False
                count += 1
        # odd case 
        else:
            count += 1
            while count <= mid:
                if w[mid-count] != w[-mid-1+count]:
                    return False
                count += 1 

        return True