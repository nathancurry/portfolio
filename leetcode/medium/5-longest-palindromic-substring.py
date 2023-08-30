"""
Took a lot of trial and error. Required additional handling for patterns from
index 0, as well as for even-numbered palindromes. Slicing indexing was also
unintuitive to me. Trade-offs teken in favor of CPU instead of memory. 
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        slen = len(s)
        longest = ""
        pals = [] 

        for c,v in enumerate(s):
            p1 = None
            p2 = None

            # special handling for 1- and 2-character strings
            if c == 0:
                n = 0
                while n < slen and s[c] == s[n]:
                    n += 1
                    p1 = s[c:n]
            
            # regular handling
            else:

                # for odd-len palindromes
                n = 1
                while c - n >= 0 and c + n < slen:
                    if s[c-1] != s[c+1]:
                        break
                    if s[c-n] == s[c+n]:
                        p1 = s[c-n:c+n+1]
                    else:
                        break
                    n += 1

                # for even-len palindromes, shift start index right
                n=1
                while c - n + 1 >= 0 and c + n < slen:
                    if s[c] != s[c+1]:
                        break
                    if s[c-n+1] == s[c+n]:
                        p2 = s[c-n+1:c+n+1]
                    else:
                        break
                    n += 1

            # save results                    
            if p1:
                pals.append(p1)
            if p2:
                pals.append(p2)

        # retrieve and compare
        for i in pals:
            if len(i) > len(longest):
                longest = i 
        return longest 
