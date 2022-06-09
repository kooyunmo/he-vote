from dataclasses import dataclass

from phe import paillier

from poll.cipher.base import CipherBase


pub_key, private_key = paillier.generate_paillier_keypair()


@dataclass
class PaillierCipher(CipherBase):
    def encrypt(self, id_: int, plaintext: int, nonce: bytes) -> int:
        return pub_key.encrypt(plaintext)

    def decrypt_sum(self, start_id: int, end_id: int, ciphertext: int, nonce: bytes) -> int:
        return private_key.decrypt(ciphertext)
