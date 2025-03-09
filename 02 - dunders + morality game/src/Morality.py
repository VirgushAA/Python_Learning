from collections import Counter
from itertools import combinations
import random


class Game(object):
    def __init__(self, matches=10):
        self.matches_: int = matches
        self.registry_ = Counter()

    def play(self, player1, player2):

        rounds = self.matches_
        while rounds:
            result = self.engine(player1.action_, player2.action_)
            self.registry_.update({player1.name_: result[0]})
            self.registry_.update({player2.name_: result[1]})
            player1.adapt(player2.action_)
            player2.adapt(player1.action_)
            rounds -= 1

    @staticmethod
    def engine(action1, action2):
        result1, result2 = 0, 0
        if action1 and action2:
            result1 += 2
            result2 += 2
        elif not action1 and action2:
            result1 += 3
            result2 -= 1
        elif action1 and not action2:
            result1 -= 1
            result2 += 3
        result: tuple = (result1, result2)
        return result

    def top3(self):
        amount: int = 3
        tmp = self.registry_.most_common(amount)
        for i in range(amount):
            print(tmp[i][0], tmp[i][1])

    def top(self, amount=3):
        tmp = self.registry_.most_common(amount)
        for i in range(amount):
            print(tmp[i][0], tmp[i][1])


class Player(object):
    def __init__(self, name):
        self.type_: str = name
        self.name_: str = 'Player'
        self.action_: bool = True

    def adapt(self, reaction):
        pass


class Cooperator(Player):
    def __init__(self, name='Cooperator'):
        super().__init__('Cooperator')
        self.name_: str = name


class Cheater(Player):
    def __init__(self, name='Cheater'):
        super().__init__('Cheater')
        self.name_: str = name
        self.action_: bool = False


class Copycat(Player):
    def __init__(self, name='Copycat'):
        super().__init__('Copycat')
        self.name_ = name

    def adapt(self, reaction):
        self.action_ = reaction


class Copykitten(Player):
    def __init__(self, name='Copykitten'):
        super().__init__('Copykitten')
        self.name_ = name
        self.distrust_: int = 0

    def adapt(self, reaction):
        if not reaction and self.distrust_ == 0:
            self.distrust_ = 1
        elif not reaction and self.distrust_ == 1:
            self.action_ = reaction
        elif reaction:
            self.action_ = True
            self.distrust_ = 0


class Simpleton(Player):
    def __init__(self, name='Simpleton'):
        super().__init__('Simpleton')
        self.name_ = name

    def adapt(self, reaction):
        if not reaction:
            self.action_ = not self.action_


class Random(Player):
    def __init__(self, name='Random'):
        super().__init__('Random')
        self.name_ = name
        self.adapt(False)

    def adapt(self, reaction):
        rand = random.randrange(0, 2, 1)
        if rand == 0:
            self.action_ = True
        elif rand == 1:
            self.action_ = False


class Grudger(Player):
    def __init__(self, name='Grudger'):
        super().__init__('Grudger')
        self.name_ = name

    def adapt(self, reaction):
        if self.action_:
            if not reaction:
                self.action_ = False


class Detective(Player):
    def __init__(self, name='Detective'):
        super().__init__('Detective')
        self.name_ = name
        self.recon_: int = 1
        self.safe_: bool = True

    def adapt(self, reaction):
        if self.recon_ < 4:
            self.recon_ += 1
            if self.recon_ != 2:
                self.action_ = True
            else:
                self.action_ = False
            if not reaction:
                self.safe_ = False
        else:
            if self.safe_:
                self.action_ = False
            else:
                self.action_ = reaction


def main():
    game = Game()

    player_list = [Cooperator, Cheater, Copycat, Grudger, Detective]

    # more players
    # player_list = [Cooperator, Cheater, Copycat, Grudger, Detective, Copykitten, Simpleton, Random]

    players = combinations(player_list, 2)

    for player1, player2 in players:
        game.play(player1(), player2())

    game.top3()


if __name__ == "__main__":
    main()
