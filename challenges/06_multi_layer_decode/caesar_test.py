# Caesar brute force on Capa 2
s = "hjhkltf{jhlzhy_k3jy9wa3k_9948kmh2}"

print("[*] Probando los 26 desplazamientos César:")
for shift in range(26):
    res = []
    for c in s:
        if 'a' <= c <= 'z':
            res.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            res.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            res.append(c)
    out = "".join(res)
    if "picoctf" in out.lower() or "academy" in out.lower() or "caesar" in out.lower() or "flag" in out.lower():
        print(f"  [+] Shift +{shift}: {out}")
    elif shift in [7, 8, 19, 20]:
        print(f"  Shift +{shift}: {out}")
