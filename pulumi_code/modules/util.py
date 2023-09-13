import hashlib
import os

def calculate_directory_hash(directory_path: str) -> str:
    sha_hash = hashlib.sha256()
    for root, dirs, files in os.walk(directory_path):
        for names in files:
            file_path = os.path.join(root, names)
            try:
                with open(file_path, "rb") as f:
                    while True:
                        data = f.read(65536)
                        if not data:
                            break
                        sha_hash.update(hashlib.sha256(data).digest())
            except IOError:
                return hashlib.sha256()
    return sha_hash
