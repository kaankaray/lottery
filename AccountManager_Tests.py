import unittest
from AccountManager import AccountManager

acc = AccountManager(randomSeed=10)


class MyTestCase(unittest.TestCase):
    def test_preset_seed_giving_correct_private_key(self):
        self.assertEqual(acc.fetchPrivKey(), '0x766bad0734c2da8003cc0f2793fdcab87b89296c6dcbac5008577eb1924770d3')

    def test_preset_seed_giving_correct_public_key(self):
        self.assertEqual(acc.fetchPublicKey(), b'26a296b96285ff81f10721ee78d3a3cea2f66e85220eac5fd60c9321aaf207f2'
                                               b'acc9a985c4e25b1d69c1d491633e3407c25c491c09445b70290368cbecccb829')

    def test_preset_seed_giving_correct_wallet(self):
        self.assertEqual(acc.walletVersion, '0xaaaa50388273174af02ebc180a2b7bacdf72a722')

if __name__ == '__main__':
    unittest.main()
