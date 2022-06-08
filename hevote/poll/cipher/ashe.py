from dataclasses import dataclass
from Crypto.Cipher import AES

from poll.cipher.base import CipherBase


@dataclass
class ASHECipher(CipherBase):
    # TODO: move to settings.py
    k: bytes = b'SgVkYp3s6v9y$B&E)H+MbQeThWmZq4t7'
    mode: int = AES.MODE_GCM

    def encrypt(self, id_: int, plaintext: int, nonce: bytes) -> int:
        id_b_1 = f'{id_-1}{nonce[0]}'.encode()
        id_b_2 = f'{id_}{nonce[0]}'.encode()
        cipher = AES.new(self.k, self.mode, nonce=id_b_1)
        c_1 = int.from_bytes(cipher.encrypt(id_b_1), 'big')
        cipher = AES.new(self.k, self.mode, nonce=id_b_2)
        c_2 = int.from_bytes(cipher.encrypt(id_b_2), 'big')
        return plaintext + c_1 - c_2

    def decrypt_sum(self, start_id: int, end_id: int, ciphertext: int, nonce: bytes) -> int:
        id_b_1 = f'{start_id}{nonce[0]}'.encode()
        id_b_2 = f'{end_id}{nonce[0]}'.encode()
        cipher = AES.new(self.k, self.mode, nonce=id_b_1)
        c_1 = int.from_bytes(cipher.encrypt(id_b_1), 'big')
        cipher = AES.new(self.k, self.mode, nonce=id_b_2)
        c_2 = int.from_bytes(cipher.encrypt(id_b_2), 'big')

        return ciphertext - c_1 + c_2
