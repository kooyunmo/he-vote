from dataclasses import dataclass

from Pyfhel import Pyfhel

from poll.cipher.base import CipherBase


he = Pyfhel()
he.load_context('he_context')
he.load_public_key('he_pub_key')
he.load_secret_key('he_sec_key')


@dataclass
class BFVCipher(CipherBase):
    def encrypt(self, id_: int, plaintext: int, nonce: bytes) -> int:
        cipher = he.encrypt(plaintext)
        return cipher

    def decrypt_sum(self, start_id: int, end_id: int, ciphertext: int, nonce: bytes) -> int:
        arr = he.decrypt(ciphertext)
        return arr[0]
