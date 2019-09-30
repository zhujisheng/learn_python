import sys
import hashlib

if len(sys.argv)!=2:
    print("Usage: file-hash.py file_name")
    exit()

file_name = sys.argv[1]

h_sha256 = hashlib.sha256()
h_md5 = hashlib.md5()
h_blake2b256 = hashlib.blake2b(digest_size=32)

with open(file_name, 'rb') as fp:
    while True:
        c = fp.read(10240)
        if not c:
            break
        h_md5.update(c)
        h_sha256.update(c)
        h_blake2b256.update(c)

print("SHA256:      ", h_sha256.hexdigest())
print("MD5:         ", h_md5.hexdigest())
print("BLAKE2b-256: ", h_blake2b256.hexdigest())
