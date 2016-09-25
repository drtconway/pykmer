# Some useful constants
m1 = 0x5555555555555555 # 01010101...
m2 = 0x3333333333333333 # 00110011...
m3 = 0x0F0F0F0F0F0F0F0F # 00001111...
m4 = 0x00FF00FF00FF00FF # 0818...
m5 = 0x0000FFFF0000FFFF # 016116...
m6 = 0x00000000FFFFFFFF # 032132

def rev(x):
    "Reverse the bit-pairs in an integer"
    x = ((x >> 2) & m2) | ((x & m2) << 2)
    x = ((x >> 4) & m3) | ((x & m3) << 4)
    x = ((x >> 8) & m4) | ((x & m4) << 8)
    x = ((x >> 16) & m5) | ((x & m5) << 16)
    x = ((x >> 32) & m6) | ((x & m6) << 32)
    return x

def popcnt(x):
    "Compute the number of set bits in a 64-bit integer"
    x = (x & m1) + ((x >> 1) & m1)
    x = (x & m2) + ((x >> 2) & m2)
    x = (x & m3) + ((x >> 4) & m3)
    x = (x & m4) + ((x >> 8) & m4)
    x = (x & m5) + ((x >> 16) & m5)
    x = (x & m6) + ((x >> 32) & m6)
    return x & 0x7F

def ffs(x):
    "Find the position of the most significant bit"
    r = (x > 0xFFFFFFFF) << 5
    x >>= r
    s = (x > 0xFFFF) << 4
    x >>= s
    r |= s
    s = (x > 0xFF) << 3
    x >>= s
    r |= s
    s = (x > 0xF) << 2
    x >>= s
    r |= s
    s = (x > 0x3) << 1
    x >>= s
    r |= s
    r |= (x >> 1)
    return r

