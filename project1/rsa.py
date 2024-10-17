import random
import sys

# This may come in handy...
from fermat import miller_rabin

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    if a < b:
        tmp = a
        a = b
        b = tmp
    if b == 0:
        return 1, 0, a
    x1, y1, d = ext_euclid(b, a % b)
    return y1, x1 - (a // b) * y1, d

# Helper function for get_relative_prime(n: int), which is a helper function for generate_key_pairs()
def euclid(N: int, e: int) -> int:
    if e == 0:
        return N
    return euclid(e, N % e)

# Helper function for generate_key_pairs()
def get_relative_prime(n: int) -> int:
    for i in primes:
        if euclid(n,i) == 1:
            return i
    return -1

# Implement this function
def generate_large_prime(bits=512) -> int:
    """
    Generate a random prime number with the specified bit length.
    Use random.getrandbits(bits) to generate a random number of the
     specified bit length.
    """
    p = random.getrandbits(bits)
    while miller_rabin(p,100) != "prime":
        p = random.getrandbits(bits)
    return p  # Guaranteed random prime number obtained through fair dice roll


# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Return N, e, d
    - N must be the product of two random prime numbers p and q
    - e and d must be multiplicative inverses mod (p-1)(q-1)
    """
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    e = get_relative_prime((p-1) * (q-1))
    while e == -1 or p == q:
        p = generate_large_prime(bits)
        q = generate_large_prime(bits)
        e = get_relative_prime((p-1) * (q-1))

    N = p*q
    
    d = ext_euclid(e,(p-1)*(q-1))[1]
    d = d % ((p-1) * (q-1))
    return N, e, d
