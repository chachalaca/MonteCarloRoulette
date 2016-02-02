__author__ = 'chachalaca'

from Roulette import Roulette
from Strategy import Strategy

class Fibonacci(Strategy):

    def __init__(self, init_bet: float, cash: float, roulette: Roulette):
        self.init_bet = init_bet
        self.cash = cash
        self.roulette = roulette

    def fib(self, n):
        if n < 2:
            return n
        return self.fib(n-2) + self.fib(n-1)

    def play(self):
        history = []
        bet = self.init_bet
        cash = self.cash

        fib = 0

        while cash >= bet <= self.roulette.max_bet:
            history.append({"cash": cash, "bet": bet})

            cash -= bet
            r = self.roulette.bet_on_color(bet)
            cash += r

            if r == 0:
                fib += 1
                bet = self.fib(fib)
            else:
                fib = max(fib-2, 0)
                bet = self.fib(fib)

        return history

    def play_for(self, goal, all_in=True):
        bet = self.init_bet
        cash = self.cash

        fib = 0

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
                fib += 1
            else:
                fib = max(fib-2, 0)

            bet = self.fib(fib)

        return True
