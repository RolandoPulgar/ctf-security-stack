import hashlib
import struct
import decimal

# Generación matemática exacta de las 80 constantes K de SHA-512
def generate_k80():
    primes = []
    c = 2
    while len(primes) < 80:
        if all(c % p != 0 for p in primes):
            primes.append(c)
        c += 1
    decimal.getcontext().prec = 100
    k80 = []
    for p in primes:
        root = decimal.Decimal(p) ** (decimal.Decimal(1) / decimal.Decimal(3))
        frac = root - int(root)
        k80.append(int(frac * (decimal.Decimal(2)**64)))
    return k80

K = generate_k80()

def ror(x, y):
    return (((x & 0xFFFFFFFFFFFFFFFF) >> (y & 63)) | (x << (64 - (y & 63)))) & 0xFFFFFFFFFFFFFFFF

def Ch(x, y, z):
    return (x & y) ^ (~x & z)

def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def Sigma0(x):
    return ror(x, 28) ^ ror(x, 34) ^ ror(x, 39)

def Sigma1(x):
    return ror(x, 14) ^ ror(x, 18) ^ ror(x, 41)

def sigma0(x):
    return ror(x, 1) ^ ror(x, 8) ^ ((x & 0xFFFFFFFFFFFFFFFF) >> 7)

def sigma1(x):
    return ror(x, 19) ^ ror(x, 61) ^ ((x & 0xFFFFFFFFFFFFFFFF) >> 6)

def sha512_padding(length_in_bytes):
    length_in_bits = length_in_bytes * 8
    pad = b'\x80'
    pad_len = (128 - ((length_in_bytes + 1 + 16) % 128)) % 128
    pad += b'\x00' * pad_len
    pad += struct.pack('>QQ', 0, length_in_bits)
    return pad

def sha512_compress_block(state, block):
    W = list(struct.unpack('>16Q', block))
    for t in range(16, 80):
        W.append((sigma1(W[t-2]) + W[t-7] + sigma0(W[t-15]) + W[t-16]) & 0xFFFFFFFFFFFFFFFF)
        
    a, b, c, d, e, f, g, h = state
    for t in range(80):
        T1 = (h + Sigma1(e) + Ch(e, f, g) + K[t] + W[t]) & 0xFFFFFFFFFFFFFFFF
        T2 = (Sigma0(a) + Maj(a, b, c)) & 0xFFFFFFFFFFFFFFFF
        h = g
        g = f
        f = e
        e = (d + T1) & 0xFFFFFFFFFFFFFFFF
        d = c
        c = b
        b = a
        a = (T1 + T2) & 0xFFFFFFFFFFFFFFFF
        
    return [
        (state[0] + a) & 0xFFFFFFFFFFFFFFFF,
        (state[1] + b) & 0xFFFFFFFFFFFFFFFF,
        (state[2] + c) & 0xFFFFFFFFFFFFFFFF,
        (state[3] + d) & 0xFFFFFFFFFFFFFFFF,
        (state[4] + e) & 0xFFFFFFFFFFFFFFFF,
        (state[5] + f) & 0xFFFFFFFFFFFFFFFF,
        (state[6] + g) & 0xFFFFFFFFFFFFFFFF,
        (state[7] + h) & 0xFFFFFFFFFFFFFFFF,
    ]

def sha512_extend(original_hash_hex, orig_len_bytes, extension_bytes):
    state = list(struct.unpack('>8Q', bytes.fromhex(original_hash_hex)))
    
    pad = sha512_padding(orig_len_bytes)
    total_len = orig_len_bytes + len(pad) + len(extension_bytes)
    
    data_to_process = extension_bytes + sha512_padding(total_len)
    for i in range(0, len(data_to_process), 128):
        block = data_to_process[i:i+128]
        state = sha512_compress_block(state, block)
        
    new_hash = "".join(f"{x:016x}" for x in state)
    return pad, new_hash

if __name__ == '__main__':
    salt = b"A" * 256
    orig = b"12, 34"
    h_orig = hashlib.sha512(salt + orig).hexdigest()
    
    ext = b", 56, 78"
    pad, h_ext = sha512_extend(h_orig, len(salt + orig), ext)
    
    expected = hashlib.sha512(salt + orig + pad + ext).hexdigest()
    print("Calculado:", h_ext)
    print("Esperado  :", expected)
    print("COINCIDENCIA EXACTA:", h_ext == expected)
