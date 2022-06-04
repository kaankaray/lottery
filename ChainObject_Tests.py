import os
import unittest
from ChainObject import Chain

exChain = Chain(name="Rinkeby", baseURL="https://api-rinkeby.etherscan.io/api")
print(exChain)


class MyTestCase(unittest.TestCase):
    def test_API_key_exists(self):
        self.assertIsNotNone(os.environ.get(f'API_{exChain.name}'))




if __name__ == '__main__':
    unittest.main()


