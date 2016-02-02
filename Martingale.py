__author__ = 'chachalaca'

from Roulette import Roulette
from Strategy import Strategy

class Martingale(Strategy):

    def __init__(self, bet: float, cash: float, roulette: Roulette):
        self.init_bet = bet
        self.cash = cash
        self.roulette = roulette

    def play(self):
        history = []
        bet = self.init_bet
        cash = self.cash

        while cash >= bet <= self.roulette.max_bet:
            history.append({"cash": cash, "bet": bet})

            cash -= bet
            r = self.roulette.bet_on_color(bet)
            cash += r

            if r == 0:
                bet *= 2
            else:
                bet = self.init_bet

        return history

    def play_for(self, goal, all_in=True):
        bet = self.init_bet
        cash = self.cash

        while cash < goal:

            if cash < self.roulette.min_bet:
                return False

            if all_in is False and (bet > self.roulette.max_bet or bet > cash):
                return False

            bet = min(bet, self.roulette.max_bet)

            if bet > cash:
                bet = cash # go all in

            cash -= bet
            r = self.roulette.bet_on_color(bet)
            cash += r

            if r == 0:
                bet *= 2
            else:
                bet = self.init_bet

        return True
