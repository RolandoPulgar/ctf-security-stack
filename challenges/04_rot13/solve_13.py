# Solver para 13 (segunda ronda de ROT13 - picoCTF)
import codecs

ciphertext = "npnqrzl{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_5p5s5o36}"
flag = codecs.decode(ciphertext, 'rot_13')

print("=" * 50)
print(f"[+] CIPHERTEXT: {ciphertext}")
print(f"[+] FLAG DESENCRIPTADA: {flag}")
print("=" * 50)
