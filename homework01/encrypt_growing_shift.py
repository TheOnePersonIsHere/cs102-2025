def encrypt_growing_shift(plaintext: str, start: int = 1, delta: int = 1) -> str:
    temp = plaintext.replace("ё", "ж").replace("Ё", "Ж")
    ciphertext = ""
    current = start
    for char in temp:
        if char.isalpha():
            if char.isupper():
                base = ord("А")
            elif char.islower():
                base = ord("а")
            new_char = (ord(char) - base + current) % 33 + base
            ciphertext += chr(new_char)
            current += delta
        else:
            ciphertext += char
    return ciphertext


result = encrypt_growing_shift("Пётон")
print(result)
