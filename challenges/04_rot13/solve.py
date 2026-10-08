# Solver para ROT13 (Cifrado César con desplazamiento 13)
import codecs

ciphertext = "npnqrzl{abg_gbb_onq_bs_n_ceboyrz}"
flag = codecs.decode(ciphertext, 'rot_13')

print("=" * 50)
print(f"[+] CIPHERTEXT: {ciphertext}")
print(f"[+] FLAG DESENCRIPTADA: {flag}")
print("=" * 50)
