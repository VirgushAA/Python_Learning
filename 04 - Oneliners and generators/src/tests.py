import unittest
from unittest.mock import patch
import io
from energy import fix_wiring
from personality import turrets_generator


class TestingPortal(unittest.TestCase):

    def test_fix_wiring_good(self):
        plugs = ['plug1', 'plug2', 'plug3']
        sockets = ['socket1', 'socket2', 'socket3', 'socket4']
        cables = ['cable1', 'cable2', 'cable3', 'cable4']
        ex = ['plug cable1 into socket1 using plug1',
              'plug cable2 into socket2 using plug2',
              'plug cable3 into socket3 using plug3',
              'weld cable4 to socket4 without plug']
        result = fix_wiring(cables, sockets, plugs)
        for i, j in zip(ex, result):
            self.assertEqual(i, j)

    def test_fix_wiring_scrambled(self):
        plugs = ['plugZ', None, 'plugY', 'plugX']
        sockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']
        cables = ['cable2', 'cable1', False]
        ex = ['plug cable2 into socket1 using plugZ',
              'plug cable1 into socket2 using plugY']
        result = fix_wiring(cables, sockets, plugs)
        for i, j in zip(ex, result):
            self.assertEqual(i, j)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_turret_generator(self, mock_stdout):
        turret = turrets_generator()
        self.assertEqual(turret.personality_traits['neuroticism'] + turret.personality_traits['openness']
                         + turret.personality_traits['conscientiousness'] + turret.personality_traits['extraversion']
                         + turret.personality_traits['agreeableness'], 100)
        turret.shoot()
        turret.search()
        turret.talk()
        output = mock_stdout.getvalue()
        out_lines = output.strip().split('\n')
        self.assertEqual(out_lines[0], 'Shooting')
        self.assertEqual(out_lines[1], 'Searching')
        self.assertEqual(out_lines[2], 'Talking')


if __name__ == '__main__':
    unittest.main()