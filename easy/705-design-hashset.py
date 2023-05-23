"""
This is a terrible and simplistic hash function, but it works.
"""

class MyHashSet:
    def __init__(self):
        self.keys = [[]] * 10

    def add(self, key: int) -> None:
        slot = self.hash(key)
        for k in self.keys[slot]:
            if key == k:
                return
        self.keys[slot].append(key)

    def remove(self, key: int) -> None:
        slot = self.hash(key)
        for k in self.keys[slot]:
            if key == k:
                self.keys[slot].remove(key)

    def contains(self, key: int) -> bool:
        slot = self.hash(key)
        for k in self.keys[slot]:
            if key == k:
                return True
        return False 

    def hash(self, key):
        return key % 10



# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)