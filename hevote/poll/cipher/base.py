from typing import Optional


class CipherBase:
    def encrypt(self, id_: Optional[int], plaintext: int, nonce: bytes) -> int:
        raise NotImplementedError

    def decrypt_sum(self, start_id: Optional[int], end_id: Optional[int], ciphertext: int, nonce: bytes) -> int:
        raise NotImplementedError
