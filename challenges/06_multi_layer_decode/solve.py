# Solver para reto de decodificación multicapa (Base64 doble + Cifrado César)
import base64

ciphertext_b64 = "YidhR3BvYTJ4MFpudHFhR3g2YUhsZmF6TnFlVGwzWVROclh6azVORGhyYldneWZRPT0nCg=="

# Paso 1: Primer Base64
step1 = base64.b64decode(ciphertext_b64).decode('utf-8').strip()
if step1.startswith("b'") and step1.endswith("'"):
    step1 = step1[2:-1]

# Paso 2: Segundo Base64
step2 = base64.b64decode(step1).decode('utf-8').strip()

# Paso 3: Cifrado César (Shift +19 / Rot-7)
def caesar_decode(text, shift=19):
    res = []
    for c in text:
        if 'a' <= c <= 'z':
            res.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            res.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            res.append(c)
    return "".join(res)

flag = caesar_decode(step2, shift=19)

print("=" * 60)
print(f"[+] Entrada Original : {ciphertext_b64}")
print(f"[+] Capa 1 (Base64)  : {step1}")
print(f"[+] Capa 2 (Base64)  : {step2}")
print(f"[+] Capa 3 (César +19): {flag}")
print("=" * 60)
