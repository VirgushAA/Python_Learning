import unittest
import Morality

class TestMorality(unittest.TestCase):

    def test_Player_Creation(self):
        p1 = Morality.Player('Player')
        self.assertEqual(p1.name_, 'Player')
        self.assertEqual(p1.type_, 'Player')
        self.assertEqual(p1.action_, True)

    def test_Cooperator_Creation(self):
        p1 = Morality.Cooperator('Cooperator_test')
        self.assertEqual(p1.name_, 'Cooperator_test')
        self.assertEqual(p1.type_, 'Cooperator')
        self.assertEqual(p1.action_, True)

    def test_Cheater_Creation(self):
        p1 = Morality.Cheater('Cheater_test')
        self.assertEqual(p1.name_, 'Cheater_test')
        self.assertEqual(p1.type_, 'Cheater')
        self.assertEqual(p1.action_, False)

    def test_Copycat_Creation(self):
        p1 = Morality.Copycat('Copycat_test')
        self.assertEqual(p1.name_, 'Copycat_test')
        self.assertEqual(p1.type_, 'Copycat')
        self.assertEqual(p1.action_, True)

    def test_Grudger_Creation(self):
        p1 = Morality.Grudger('Grudger_test')
        self.assertEqual(p1.name_, 'Grudger_test')
        self.assertEqual(p1.type_, 'Grudger')
        self.assertEqual(p1.action_, True)

    def test_Detective_Creation(self):
        p1 = Morality.Detective('Detective_test')
        self.assertEqual(p1.name_, 'Detective_test')
        self.assertEqual(p1.type_, 'Detective')
        self.assertEqual(p1.action_, True)

    def test_Copycat_adapt(self):
        p1 = Morality.Copycat()
        self.assertTrue(p1.action_)
        p1.adapt(True)
        self.assertTrue(p1.action_)
        p1.adapt(False)
        self.assertFalse(p1.action_)

    def test_Copykitten_adapt(self):
        p1 = Morality.Copykitten()
        self.assertTrue(p1.action_)
        p1.adapt(True)
        self.assertTrue(p1.action_)
        p1.adapt(False)
        self.assertTrue(p1.action_)
        p1.adapt(False)
        p1.adapt(False)
        self.assertFalse(p1.action_)

    def test_Simpleton_adapt(self):
        p1 = Morality.Simpleton()
        self.assertTrue(p1.action_)
        p1.adapt(True)
        self.assertTrue(p1.action_)
        p1.adapt(False)
        self.assertFalse(p1.action_)
        p1.adapt(True)
        self.assertFalse(p1.action_)
        p1.adapt(False)
        self.assertTrue(p1.action_)

    def test_Grudger_adapt(self):
        p1 = Morality.Grudger()
        self.assertTrue(p1.action_)
        p1.adapt(True)
        self.assertTrue(p1.action_)
        p1.adapt(False)
        self.assertFalse(p1.action_)

    def test_Detective_adapt_abuse(self):
        p1 = Morality.Detective()
        self.assertTrue(p1.action_)
        p1.adapt(True)
        self.assertFalse(p1.action_)
        p1.adapt(True)
        p1.adapt(True)
        p1.adapt(True)
        self.assertFalse(p1.action_)

    def test_Detective_adapt_copy(self):
        p1 = Morality.Detective()
        self.assertTrue(p1.action_)
        p1.adapt(False)
        self.assertFalse(p1.action_)
        p1.adapt(True)
        p1.adapt(True)
        p1.adapt(True)
        self.assertTrue(p1.action_)
        p1.adapt(False)
        self.assertFalse(p1.action_)

    def test_Game_creation(self):
        game = Morality.Game()
        self.assertEqual(game.matches_, 10)
        self.assertEqual(game.registry_, {})
        game_1 = Morality.Game(100)
        self.assertEqual(game_1.matches_, 100)
        self.assertEqual(game_1.registry_, {})

    def test_engine(self):
        game = Morality.Game()
        self.assertEqual(game.engine(Morality.Cooperator().action_, Morality.Cheater().action_), (-1, 3))
        self.assertEqual(game.engine(Morality.Cheater().action_, Morality.Cooperator().action_), (3, -1))
        self.assertEqual(game.engine(Morality.Cooperator().action_, Morality.Cooperator().action_), (2, 2))
        self.assertEqual(game.engine(Morality.Cheater().action_, Morality.Cheater().action_), (0, 0))

    def test_Play(self):
        game = Morality.Game()
        game.play(Morality.Cheater(), Morality.Cooperator())
        self.assertEqual(game.registry_, {'Cheater': 30, 'Cooperator': -10})


if __name__ == '__main__':
    unittest.main()