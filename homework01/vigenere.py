def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            key_char = keyword[key_index % len(keyword)]

            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            shift = ord(key_char.upper()) - ord('A')

            new_char = (ord(char) - base + shift) % 26 + base
            ciphertext += chr(new_char)

            key_index += 1
        else:
            ciphertext += char

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            key_char = keyword[key_index % len(keyword)]

            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            shift = ord(key_char.upper()) - ord('A')

            original_char = (ord(char) - base - shift + 26) % 26 + base
            plaintext += chr(original_char)

            key_index += 1
        else:
            plaintext += char

    return plaintext