"""
Not particularly efficient. I have ideas about how to approach, but I'm moving
on for now. Build a matrix, and then walk the matrix per spec. This could be
much neater with some functions.
"""

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # base case
        if numRows == 1:
            return s

        # output matrix
        matrix = []

        # control variables for nested loops
        i = 0
        col = 0
        slen = len(s)
        zaglen = numRows - 2
        zig = True

        # while loop so I can freely increment `i`
        while i < slen:
            # zig down
            if zig:
                row = 0
                matrix.append([])
                while row < numRows:
                    if i >= slen:
                        break
                    else:
                        matrix[col].append(s[i])
                    i += 1
                    row += 1
                col += 1
                zig = False

            # zag across and up
            else:
                row = 1
                while row <= zaglen:
                    if i >= slen:
                        break
                    else:
                        matrix.append([''] * numRows)
                        matrix[col][numRows - row - 1] = s[i]
                    i += 1
                    row += 1
                    col += 1
                zig = True
        
        # build output string
        os = ""
        for row in range(numRows):
                for col in matrix:
                    if row < len(col):
                        os += col[row]
        return os