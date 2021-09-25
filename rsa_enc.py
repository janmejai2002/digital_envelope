import random

def key_gen(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False
        if isPrime:
            prime_list.append(n)
    randomPrime1 = random.choice(prime_list)
    randomPrime2 = random.choice(prime_list)
    return (randomPrime1, randomPrime2)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def crypt_keygen():
    p,q = key_gen(2,100)
    n = p * q
    phi = (p-1) * (q-1)
    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    #Use Extended Euclid's Algorithm to generate the private key
    d = mod_inverse(e,phi)
    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    # print(f"key --> {key} | n --> {n} | ct --> {ciphertext} | {type(ciphertext)}")
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


def rsa(message):
    public, private = crypt_keygen()
    encrypted_message = encrypt(private, message)
    decrypted_message = decrypt(public, encrypted_message)
    return encrypted_message, decrypted_message

def main():
    message = input("Please enter your message : ")
    encrypted, decrypted = rsa(message)
    print(f"Encrypted Message : {''.join(map(lambda x: str(x), encrypted))}")
    print(f"Decrypted Message : {decrypted}")

if __name__ == '__main__':
    main()