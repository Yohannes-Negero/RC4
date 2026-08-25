#!/usr/bin/env python3
"""
RC4 File Decryptor
Decrypts the contents of file.txt in-place using the same RC4 key.
Because RC4 is a symmetric stream cipher, decryption is identical to encryption.
"""

import sys

# Must match the key used by the encryptor
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

    # Open encrypted file in binary mode
    with open(filename, "rb") as f:
        ciphertext = f.read()

    if not ciphertext:
        print(f"[!] {filename} is empty – nothing to decrypt.")
        return

    # Decrypt (same operation as encrypt)
    plaintext = rc4(ciphertext, KEY)

    # Write restored bytes back
    with open(filename, "wb") as f:
        f.write(plaintext)

    print(f"[+] Decrypted {len(ciphertext)} bytes → {filename}")
    print(f"    Key used: {KEY!r}")
    print(f"    Restored content preview:\n{plaintext[:200].decode(errors='replace')}")


if __name__ == "__main__":
    main()
