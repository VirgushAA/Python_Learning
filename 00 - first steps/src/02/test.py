import mfinder
import unittest

arr = {"*   *", "** **", "* * *"}

class TestsM(unittest.TestCase):

    def test_1(self):
        self.assertEqual(mfinder, 'True')
        # self.assertEqual("True", 'True')

    t = mfinder


if __name__ == '__main__':
    unittest.main()