"""
I tried this without using an out variable and changing every assignment to a
return statement, but that was significantly slower.
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        out = 0
        # base case
        if root is None:
            return 0
        # recurse and return maximum
        if root.left and root.right:
            out = max([self.maxDepth(root.left), self.maxDepth(root.right)])
        elif root.left:
            out = self.maxDepth(root.left)
        elif root.right:
            out = self.maxDepth(root.right)
        out += 1
        return out