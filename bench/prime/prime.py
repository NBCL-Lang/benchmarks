def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def count_primes(limit):
    count = 0
    for i in range(1, limit):
        if is_prime(i):
            count += 1
    return count

print(count_primes(10000))