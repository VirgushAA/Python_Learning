import unittest
import purse

class TestPurseFuncs(unittest.TestCase):

    def test_add_ingot(self):
        self.assertEqual(purse.add_ingot({'gold_ingots': 3}), {'gold_ingots': 4})
        
    def test_add_ingot_empty(self):
        self.assertEqual(purse.add_ingot({}), {'gold_ingots': 1})
        
    def test_get_ingot(self):
        self.assertEqual(purse.get_ingot({'gold_ingots': 3}), {'gold_ingots': 2})

    def test_get_ingot_empty(self):
        self.assertEqual(purse.get_ingot({}), {})

    def test_empty(self):
        self.assertEqual(purse.empty({'gold_ingots': 3}), {})
    
    def test_split_booty(self):
        self.assertEqual(purse.split_booty({"gold_ingots": 100}, {"gold_slabs": 1000}, {"gold_ingots": -200}, {"gold_ingots":100}), ({'gold_ingots': 67}, {'gold_ingots': 67}, {'gold_ingots': 66}))

    def test_split_booty_empty(self):
        self.assertEqual(purse.split_booty({}), ({'gold_ingots': 0}, {'gold_ingots': 0}, {'gold_ingots': 0}))

if __name__ == '__main__':
    unittest.main()