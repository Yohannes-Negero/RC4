#!/usr/bin/env python3
"""
RC4 File Encryptor
Encrypts the contents of file.txt in-place using the RC4 stream cipher.
"""

import sys


KEY = b"SecretRC4Key123!"


def rc4(data: bytes, key: bytes) -> bytes:
    """RC4 stream cipher (encryption == decryption)."""
    # Key-Scheduling Algorithm (KSA)
    S = list(range(256))
    j = 0
    key_len = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        out.append(byte ^ k)
    return bytes(out)


def main():
    filename = "file.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    # 1. Open file in binary mode
    with open(filename, "rb") as f:
        # 2. Read contents into memory buffer
        plaintext = f.read()

    if not plaintext:
        print(f"[!] {filename} is empty – nothing to encrypt.")
        return

    # 3. Encrypt the bytes using RC4
    ciphertext = rc4(plaintext, KEY)

    # 4. Write encrypted bytes back to the same file
    with open(filename, "wb") as f:
        f.write(ciphertext)

    print(f"[+] Encrypted {len(plaintext)} bytes → {filename}")
    print(f"    Key used: {KEY!r}")
    print(f"    First 32 bytes of ciphertext (hex): {ciphertext[:32].hex()}")


if __name__ == "__main__":
    main()
