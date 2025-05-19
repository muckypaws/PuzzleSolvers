#!/usr/bin/env python3
"""
RSA Decryption using Fermat's Factorisation
Includes round-trip check to confirm encryption/decryption correctness.
Written for educational purposes by Jason Brooks & ChatGPT
"""

from sympy import Integer, sqrt, ceiling, isprime, mod_inverse

# --- Configuration ---
n = Integer(238906828912334428985678707283137258157)
e = Integer(65537)
c = Integer(86594218145090370142827105263995549926)


# --- Fermat Factorisation ---
def fermat_factor(n):
    print("[*] Starting Fermat's factorisation...")
    a = ceiling(sqrt(n))
    b2 = a * a - n
    attempt = 0

    while True:
        b = sqrt(b2)
        if b == int(b):
            p = a - b
            q = a + b
            if isprime(p) and isprime(q):
                print(f"[+] Factors found on attempt {attempt}:")
                return int(p), int(q)
        a += 1
        b2 = a * a - n
        attempt += 1


# --- Convert Integer to Plaintext ---
def int_to_text(m):
    m_int = int(m)
    m_bytes = m_int.to_bytes((m_int.bit_length() + 7) // 8, byteorder='big')
    try:
        return m_bytes.decode()
    except UnicodeDecodeError:
        return m_bytes.decode(errors='ignore')


# --- Convert Plaintext to Integer ---
def text_to_int(plaintext):
    return int.from_bytes(plaintext.encode(), byteorder='big')

# --- Main Execution ---
def main():
    print("[*] RSA modulus (n):", n)
    print("[*] Public exponent (e):", e)
    print("[*] Ciphertext (c):", c)

    p, q = fermat_factor(n)

    print(f"    p = {p}")
    print(f"    q = {q}")

    phi_n = (p - 1) * (q - 1)
    d = int(mod_inverse(e, phi_n))
    m = int(pow(c, d, n))
    plaintext = int_to_text(m)

    print("[*] φ(n):", phi_n)
    print("[*] Private exponent (d):", d)
    print("[*] Decrypted integer:", m)
    print("[*] Decrypted message:", plaintext)

    # --- Round-Trip Check ---
    print("\n[*] Performing round-trip verification...")
    m_check = text_to_int(plaintext)
    c_check = pow(m_check, int(e), int(n))


    print("[*] Re-encrypted ciphertext:", c_check)
    if c_check == c:
        print("[✓] Match confirmed: encryption and decryption are consistent.")
    else:
        print("[✗] Mismatch detected: something's off.")

if __name__ == "__main__":
    main()
