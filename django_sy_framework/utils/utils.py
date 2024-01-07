import hashlib

BUF_SIZE = 65536


def make_file_hash(file_to_hash):
    sha256 = hashlib.sha256()
    while True:
        data = file_to_hash.read(BUF_SIZE)
        if not data:
            break

        sha256.update(data)

    return sha256.hexdigest()
