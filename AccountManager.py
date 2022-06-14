import logging
import random
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak
import codecs


class AccountManager(object):
    """
    Ether account creator and converter
    """

    _privateKey = '0'
    _publicKey = '0'
    walletVersion = '0'

    def fetchPrivKey(self):
        return self._privateKey

    def fetchPublicKey(self):
        return self._publicKey

    def _privKeyToPublic(self, inputByte):
        private_key_bytes = codecs.decode(inputByte, 'hex')
        key = SigningKey.from_string(private_key_bytes, curve=SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        # logging.debug(f'{inputByte} -> {key_hex}')
        return key_hex

    def _publicKeyToWallet(self, inputByte):
        public_key_bytes = codecs.decode(inputByte, 'hex')
        keccak_digest = keccak.new(digest_bits=256).update(public_key_bytes).hexdigest()
        # logging.debug(f'{inputByte} -> {"0x" + keccak_digest[-40:]}')
        return '0x' + keccak_digest[-40:]

    def __init__(self, privKey=None, randomSeed=10):
        random.seed(randomSeed)
        while len(self._privateKey) != 66:
            self._privateKey = privKey if privKey else str(hex(random.getrandbits(256)))
        self._publicKey = self._privKeyToPublic(self._privateKey[2:])
        self.walletVersion = self._publicKeyToWallet(self._publicKey)

        logging.debug(f'Wallet created: {self.walletVersion}')
