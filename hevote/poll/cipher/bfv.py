from dataclasses import dataclass
from pathlib import Path

from Pyfhel import Pyfhel

from poll.cipher.base import CipherBase


context = Path('he_context')
pub_key = Path('he_pub.key')
secret_key = Path('he_secret.key')

he = Pyfhel()
if context.exists():
    assert pub_key.exists()
    assert secret_key.exists()
    he.load_context(context)
    he.load_public_key(pub_key)
    he.load_secret_key(secret_key)
else:
    he.contextGen('bfv', n=2 ** 13, t=65537)
    he.keyGen()
    he.save_context(context)
    he.save_public_key(pub_key)
    he.save_secret_key(secret_key)


@dataclass
class BFVCipher(CipherBase):
    def encrypt(self, id_: int, plaintext: int, nonce: bytes) -> int:
        cipher = he.encrypt(plaintext)
        return cipher

    def decrypt_sum(self, start_id: int, end_id: int, ciphertext: int, nonce: bytes) -> int:
        arr = he.decrypt(ciphertext)
        return arr[0]
