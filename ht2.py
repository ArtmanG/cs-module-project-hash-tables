class HashTableEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

MIN_CAPACITY = 8


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = [None] * capacity
        self.total = 0

    def get_num_slots(self):
        return self.capacity


    def get_load_factor(self):
        return self.total / self.capacity


    def fnv1(self, key):
        FNV_prime = 1099511628211
        offset_basis = 14695981039346656037

        hash = offset_basis
        for x in key:
            hash = hash * FNV_prime
            hash = hash ^ ord(x)
        return hash

    def djb2(self, key):
        hash = 5381
        for x in key:
            hash = (hash * 33) + ord(x)
        return hash


    def hash_index(self, key):
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        index = self.hash_index(key)
        current = self.storage[index]

        if current:
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next:
                    current = current.next
                else:
                    current.next = HashTableEntry(key, value)
                    self.total += 1
         
        else:
            self.storage[index] = HashTableEntry(key, value)
            self.total += 1

        if self.get_load_factor() >= 0.7:
            self.resize(self.capacity * 2)


    def delete(self, key):
        index = self.hash_index(key)
        current = self.storage[index]

        if current:
            while current:
                if current.key == key:
                    self.total -= 1
                    self.storage[index] = current.next
                    if self.capacity > 16:
                        self.resize(self.capacity / 2)
                    return
                elif current.next:
                    current = current.next
                else:
                    return
        else:
            return    


    def get(self, key):
        current = self.storage[self.hash_index(key)]

        if current:
            while current.next:
                if current.key == key:
                    return current.value
                else:
                    current = current.next
            if current.key == key:
                return current.value
        return


    def resize(self, new_capacity):
        prev_storage = self.storage
        self.capacity = new_capacity
        self.storage = [None] * self.storage
        
        for index in prev_storage:
            if index:
                self.storage[self.hash_index(index.key)] = index
                current = index.next
                while current:
                    self.storage[self.hash_index(current.key)] = current
                    current = current.next

                    

if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")