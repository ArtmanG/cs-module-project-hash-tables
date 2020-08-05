class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # total slots in the array
        self.capacity = capacity
        # items currently in array default is None in each slot
        self.storage = [None] * capacity
        # total to track number of things added into this hash table
        self.total = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Length of hash table
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.total / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        FNV_prime = 1099511628211
        offset_basis = 14695981039346656037

        hash = offset_basis
        for x in key:
            hash = hash * FNV_prime
            hash = hash ^ ord(x)
        return hash

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = (hash * 33) + ord(x)
        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        
        # use the key to get the index
        index = self.hash_index(key)
        # var for what is at the index
        current = self.storage[index]

        # if there is something at the current index
        if current:
            # while at the current
            while current:
                # if the current's key equals the input key 
                if current.key == key:
                    # overwrite the value
                    current.value = value
                    return
                # if there is a next
                if current.next:
                    # the next is now the current and we start again
                    current = current.next
                # once we check that all the keys are original and we still have this one, add it to the end of the list
                else:
                    current.next = HashTableEntry(key, value)
                    # we added something, up the total
                    self.total += 1
                    
        # nothing is at this index, add it          
        else:
            self.storage[index] = HashTableEntry(key, value)
            # we added something, up the total
            self.total += 1

        # check if we are running out of space in our hash table
        if self.get_load_factor() >= 0.7:
            # double the size
            self.resize(self.capacity * 2)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # use the key to get the index
        index = self.hash_index(key)
        # var for what is at the index
        current = self.storage[index]

        # if there is something at the current index
        if current:
            # while there is something at the current 
            while current:
                # if the current's key equals the key we are looking for
                if current.key == key:
                    # the total things in the hash table is one less
                    self.total -= 1
                    # delete it from the list (the index here is now equal to what was the next index) 
                    self.storage[index] = current.next
                    # check if the capacity is too big. (like is it double the initial array size)
                    if self.capacity > 16:
                        self.resize(self.capacity / 2)
                    return
                # else we move on to the next one and check again
                elif current.next:
                    current = current.next
                # else it wasn't there and we can't delete anything
                else:
                    return
        # nothing to delete
        else:
            return    


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        current = self.storage[self.hash_index(key)]

        # if there is something at current
        if current:
            # while there is a next
            while current.next:
                # if the currents key matches the 
                if current.key == key:
                    return current.value
                # else move on to the next
                else:
                    current = current.next
            # when there is no next
            if current.key == key:
                return current.value
        # either you've found what you are looking for or you are returning None
        return


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # set the previous storage as the current storage
        prev_storage = self.storage
        # the capacity is now the new capacity
        self.capacity = new_capacity
        # the current storage becomes the new storage by none * new capacity
        self.storage = [None] * new_capacity
        
        # loop through in the old storage
        for index in prev_storage:
            # if the index has anything in it
            if index:
                # set the new index for it in the new storage by hashing again 
                self.storage[self.hash_index(index.key)] = index
                # does this have a next? is it part of a linked list
                current = index.next
                # if it does
                while current:
                    # rehash it and give it a new index
                    self.storage[self.hash_index(current.key)] = current
                    # do it all again until there is no next
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
