from dataclasses import dataclass
from Crypto.Cipher import AES

from poll.cipher.base import CipherBase


@dataclass
class ASHECipher(CipherBase):
    # TODO: move to settings.py
    k: bytes = b'Sixteen byte key'
    mode: int = AES.MODE_EAX

    def encrypt(self, id_: int, plaintext: int, nonce: bytes) -> int:
        cipher = AES.new(self.k, self.mode, nonce=nonce)
        id_b_1 = bin(id_).encode()
        id_b_2 = bin(id_ - 1).encode()
        c_1 = int.from_bytes(cipher.encrypt(id_b_1), 'big')
        c_2 = int.from_bytes(cipher.encrypt(id_b_2), 'big')
        return plaintext - c_1 + c_2

    def decrypt_sum(self, start_id: int, end_id: int, ciphertext: int, nonce: bytes) -> int:
        cipher = AES.new(self.k, self.mode, nonce=nonce)
        id_b_1 = bin(start_id).encode()
        id_b_2 = bin(end_id).encode()
        c_1 = int.from_bytes(cipher.encrypt(id_b_1), 'big')
        c_2 = int.from_bytes(cipher.encrypt(id_b_2), 'big')

        return ciphertext + c_2 - c_1
