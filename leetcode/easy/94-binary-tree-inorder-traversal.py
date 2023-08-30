"""
This wasn't very difficult. It looks like I got better performance out of 
list.extend(list2) vs list += list2, though I need to look into this.
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        out = []
        if root is None:
            return out
        if root.left:
            out.extend(self.inorderTraversal(root.left))
        out.append(root.val)
        if root.right:
            out.extend(self.inorderTraversal(root.right))
        return out