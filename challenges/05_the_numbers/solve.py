# Solver para A1Z26 Cipher (The Numbers - picoCTF)

nums = [
    16, 9, 3, 15, 3, 20, 6,
    "{",
    20, 8, 5,
    14, 21, 13, 2, 5, 18, 19, 13, 1,
    19, 15, 14,
    "}"
]

decoded = []
for item in nums:
    if isinstance(item, int):
        decoded.append(chr(ord('A') + item - 1))
    else:
        decoded.append(item)

flag = "".join(decoded)
print("=" * 50)
print(f"[+] FLAG DESENCRIPTADA: {flag}")
print("=" * 50)
