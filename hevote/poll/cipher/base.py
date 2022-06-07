class CipherBase:
    def encrypt(self, id_: int, plaintext: int, nonce: bytes) -> int:
        raise NotImplementedError

    def decrypt_sum(self, start_id: int, end_id: int, ciphertext: int, nonce: bytes) -> int:
        raise NotImplementedError
