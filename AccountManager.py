import logging
import random
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import keccak
import codecs


class AccountManager(object):
    """
    Ether account creator and conventer
    """

    _privateKey = '0'
    _publicKey = '0'
    walletVersion = '0'

    def fetchPrivKey(self):
        return self._privateKey

    def fetchPublicKey(self):
        return self._publicKey

    def privKeyToPublic(self, inputByte):
        private_key_bytes = codecs.decode(inputByte, 'hex')
        key = SigningKey.from_string(private_key_bytes, curve=SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        # logging.debug(f'{inputByte} -> {key_hex}')
        return key_hex

    def publicKeyToWallet(self, inputByte):
        public_key_bytes = codecs.decode(inputByte, 'hex')
        keccak_digest = keccak.new(digest_bits=256).update(public_key_bytes).hexdigest()
        # logging.debug(f'{inputByte} -> {"0x" + keccak_digest[-40:]}')
        return '0x' + keccak_digest[-40:]

    def __init__(self, randomSeed):
        random.seed(randomSeed)
        while len(self._privateKey) != 66:
            self._privateKey = str(hex(random.getrandbits(256)))
        self._publicKey = self.privKeyToPublic(self._privateKey[2:])
        self.walletVersion = self.publicKeyToWallet(self._publicKey)

        logging.info(f'Wallet created: {self.walletVersion}')
