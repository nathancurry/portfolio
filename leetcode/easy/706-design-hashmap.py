"""
This is only slightly more complext than the hash set.
"""

class MyHashMap:
    def __init__(self):
        self.keys = [[]] * 10


    def put(self, key: int, value: int) -> None:
        s = self.hash(key)
        for c,v in enumerate(self.keys[s]):
            if key == v[0]:
                self.keys[s][c] = [key, value]
                return
        self.keys[s].append([key, value])


    def get(self, key: int) -> int:
        s = self.hash(key)
        for c,v in enumerate(self.keys[s]):
            if key == v[0]:
                return v[1]
        return -1

    def remove(self, key: int) -> None:
        s = self.hash(key)
        for c,v in enumerate(self.keys[s]):
            if key == v[0]:
                self.keys[s].pop(c)
                return

    def hash(self, key) -> int:
        return key % 10      


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)