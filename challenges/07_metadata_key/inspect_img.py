import subprocess
import json
from PIL import Image
from PIL.ExifTags import TAGS

img_path = "challenges/image (1).jpg"

with open(img_path, "rb") as f:
    data = f.read()

print(f"[*] Tamaño de imagen: {len(data)} bytes")

# Buscar todas las cadenas de texto legibles o segmentos EXIF/COM/XMP
import re
text_strings = re.findall(rb'[ -~]{4,}', data)
print("[*] Cadenas de texto encontradas en el JPG:")
for s in text_strings:
    try:
        decoded = s.decode('utf-8')
        if not decoded.startswith("CDEFGHIJ"):
            print("   ", decoded)
    except:
        pass

# Revisar con PIL
try:
    img = Image.open(img_path)
    exif = img._getexif()
    if exif:
        print("\n[*] EXIF Tags:")
        for tag, value in exif.items():
            tag_name = TAGS.get(tag, tag)
            print(f"    {tag_name}: {value}")
except Exception as e:
    print(f"[-] Error leyendo EXIF con PIL: {e}")
