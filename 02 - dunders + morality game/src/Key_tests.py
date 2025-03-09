import unittest
from Key import Key

class TestKey(unittest.TestCase):

    def test_key_len(self):
        self.assertTrue(len(key) == 1337)

    def test_key_item(self):
        self.assertTrue(key[404] == 3)

    def test_key_9000(self):
        self.assertTrue(key > 9000)

    def test_key_passphrase(self):
        self.assertTrue(key.passphrase == "zax2rulez")

    def test_key_str(self):
        self.assertTrue(str(key) == "GeneralTsoKeycard")


key = Key()

if __name__ == '__main__':
    unittest.main()