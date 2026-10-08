import socket
import re
import ast
import struct
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from sha512_ext import sha512_extend

HOST = "xebec.cylabacademy.net"
PORT = 37958

def parse_vector_sim(raw_str):
    sanitized = "".join(c if c in '0123456789,[]' else '' for c in raw_str)
    try:
        parsed = ast.literal_eval(sanitized)
        if isinstance(parsed, list):
            return parsed
    except:
        pass
    return None

def recv_until(s, prompt):
    data = b""
    while not data.endswith(prompt.encode()):
        chunk = s.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode('utf-8', errors='ignore')

def attempt(host, port, attempt_num):
    print(f"\n==================== Intento #{attempt_num} ====================")
    print(f"[*] Conectando a {host}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(15)
        s.connect((host, port))
    except Exception as e:
        print(f"[-] Error de conexión: {e}")
        return None
        
    initial = recv_until(s, "Enter your vector: ")
    
    iv_match = re.search(r'IV:\s*([0-9a-fA-F]+)', initial)
    ct_match = re.search(r'Ciphertext:\s*([0-9a-fA-F]+)', initial)
    
    if not (iv_match and ct_match):
        print("[-] No se pudo extraer IV o Ciphertext")
        s.close()
        return None
        
    iv_hex = iv_match.group(1)
    ct_hex = ct_match.group(1)
    
    pairs = re.findall(r'\(\s*(\[[^\]]+\])\s*,\s*[\'"]([0-9a-fA-F]{128})[\'"]\s*\)', initial)
    print(f"[+] Vectores base confiables: {len(pairs)}")
    if len(pairs) < 5:
        s.close()
        return None
        
    matrix_rows = []
    results = []
    
    for pair_idx, (orig_vec_str, orig_hash) in enumerate(pairs):
        orig_inner = orig_vec_str[1:-1]
        orig_bytes = orig_inner.encode('latin-1')
        orig_len_bytes = 256 + len(orig_bytes)
        
        # 1. Base sin extensión
        sim_vec_base = parse_vector_sim(orig_vec_str)
        sim_row_base = sim_vec_base + [0] * (32 - len(sim_vec_base))
        sim_row_base = sim_row_base[:32]
        
        escaped_base = orig_vec_str.encode('unicode_escape').decode('latin-1')
        s.sendall((escaped_base + "\n").encode('latin-1'))
        recv_until(s, "Enter its salted hash: ")
        s.sendall((orig_hash + "\n").encode('latin-1'))
        
        resp = recv_until(s, "========================================================")
        dp_val = int(re.search(r'computed dot product is:\s*(-?\d+)', resp).group(1))
        matrix_rows.append(sim_row_base)
        results.append(dp_val)
        recv_until(s, "Enter your vector: ")
        
        # 2. Extensiones con variaciones por posición
        for ext_len in range(1, 15):
            ext_items = [str(k * 13 + ext_len * 7 + 3) for k in range(ext_len * 3)]
            ext_str = ", " + ", ".join(ext_items)
            ext_bytes = ext_str.encode('latin-1')
            
            pad, new_hash = sha512_extend(orig_hash, orig_len_bytes, ext_bytes)
            payload_full = "[" + orig_inner + pad.decode('latin-1') + ext_str + "]"
            
            sim_vec = parse_vector_sim(payload_full)
            if not sim_vec:
                continue
            sim_row = sim_vec + [0] * (32 - len(sim_vec))
            sim_row = sim_row[:32]
            
            escaped_payload = payload_full.encode('unicode_escape').decode('latin-1')
            s.sendall((escaped_payload + "\n").encode('latin-1'))
            recv_until(s, "Enter its salted hash: ")
            s.sendall((new_hash + "\n").encode('latin-1'))
            
            resp = recv_until(s, "========================================================")
            dp_match = re.search(r'computed dot product is:\s*(-?\d+)', resp)
            if dp_match:
                dp_val = int(dp_match.group(1))
                matrix_rows.append(sim_row)
                results.append(dp_val)
                
            recv_until(s, "Enter your vector: ")
            
    s.close()
    
    M_np = np.array(matrix_rows, dtype=float)
    Y_np = np.array(results, dtype=float)
    rank = np.linalg.matrix_rank(M_np)
    print(f"[*] Rango obtenido: {rank}/32 ({len(matrix_rows)} ecuaciones)")
    
    if rank == 32:
        key_sol, residuals, rank_sol, s_val = np.linalg.lstsq(M_np, Y_np, rcond=None)
        key_bytes = bytes([int(np.clip(round(k), 0, 255)) for k in key_sol])
        print(f"\n[+] ¡RANGO COMPLETO 32 ALCANZADO!")
        print(f"[+] CLAVE AES (HEX): {key_bytes.hex()}")
        
        cipher = AES.new(key_bytes, AES.MODE_CBC, bytes.fromhex(iv_hex))
        decrypted = cipher.decrypt(bytes.fromhex(ct_hex))
        try:
            flag = unpad(decrypted, AES.block_size).decode('utf-8')
        except Exception:
            flag = decrypted.decode('utf-8', errors='ignore')
            
        print("=" * 60)
        print(f"[+] FLAG DESENCRIPTADA: {flag}")
        print("=" * 60)
        return flag
        
    return None

def main():
    attempt_num = 1
    while True:
        flag = attempt(HOST, PORT, attempt_num)
        if flag and ("academy{" in flag or "picoctf{" in flag or "{" in flag):
            break
        attempt_num += 1

if __name__ == '__main__':
    main()
