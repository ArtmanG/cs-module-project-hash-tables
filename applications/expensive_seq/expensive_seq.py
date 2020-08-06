# Your code here
cache = {}

def expensive_seq(x, y, z):
    
    # defaults
    a = (x-1, y+1, z)
    b = (x-2, y+2, z*2)
    c = (x-3, y+3, z*3)

    # base case
    if x <= 0:
        return y+z
    # check the cache, if not add to cache
    elif x > 0:
        if a not in cache:
            cache[a] = expensive_seq(x-1, y+1, z)
        if b not in cache:
            cache[b] = expensive_seq(x-2, y+2, z*2)
        if c not in cache:
            cache[c] = expensive_seq(x-3, y+3, z*3)
    # add them all together
    return cache[a] + cache[b] + cache[c]


if __name__ == "__main__":
    for i in range(10):
        x = expensive_seq(i*2, i*3, i*4)
        print(f"{i*2} {i*3} {i*4} = {x}")

    print(expensive_seq(150, 400, 800))
