__author__ = 'chachalaca'

from Roulette import Roulette
import random

class FrenchRoulette(Roulette):

    def __init__(self, min_bet, max_bet):
        self.min_bet = min_bet
        self.max_bet = max_bet

    @staticmethod
    def bet_on_color(bet):

        num = random.randint(0, 36)
        if num > 0 and num % 2 == 1:
            return bet*2
        else:
            return 0
