function is_prime(n) {
    if (n <= 1) { return false }
    for (let i = 2; i < n; i++) {
        if (n % i == 0) { return false }
    }
    return true;
}

function count_primes(limit) {
    let count = 0;
    for (let i = 1; i < limit; i++) {
        if (is_prime(i)) {
            count = count + 1;
        }
    }
    return count;
}

console.log(count_primes(10000))