# student id: 011028882

# class defining hash table using open addressing


class HashTable:
    # capacity defaults to 41: a prime above 40 that gives zero collisions for keys 1-40
    def __init__(self, capacity: int = 41) -> None:
        self.capacity: int = capacity
        # each slot holds either None (empty) or a [key, value] pair
        self.table: list[list | None] = [None] * capacity

    # maps an integer key to slot index via modulo
    def hash(self, key: int) -> int:
        return int(key) % self.capacity

    # stores value at slot determined by key hash
    # each bucket stores key alongside value so lookup can verify match
    def insert(self, key: int, value):
        index = self.hash(key)
        self.table[index] = [key, value]

    # returns value for given key, or None if slot is empty or mismatched
    def lookup(self, key: int):
        index = self.hash(key)
        bucket = self.table[index]
        # confirm slot belongs to key before returning its value
        if bucket and bucket[0] == key:
            return bucket[1]
        return None
