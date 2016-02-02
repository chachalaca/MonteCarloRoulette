__author__ = 'chachalaca'

from Roulette import Roulette
from Strategy import Strategy

class Labouchere(Strategy):

    init_series = None

    def __init__(self, init_bet: float, cash: float, roulette: Roulette):
        self.init_bet = init_bet
        self.cash = cash
        self.roulette = roulette
        self.init_series = [x+init_bet for x in [0, 1, 2, 3, 4, 5]]

    def play(self):
        history = []
        bet = self.init_series[0]+self.init_series[-1]
        cash = self.cash

        series = self.init_series

        while cash >= bet <= self.roulette.max_bet:
            history.append({"cash": cash, "bet": bet})

            cash -= bet
            r = self.roulette.bet_on_color(bet)
            cash += r

            if r == 0:
                series.append(bet)
            else:
                if len(series) > 2:
                    del series[0]
                    del series[-1]
                else:
                    series = self.init_series

            bet = series[0]+series[-1]

        return history

    def play_for(self, goal, all_in=True):
        bet = self.init_bet
        cash = self.cash

        series = self.init_series

        while cash < goal:

            if cash < self.roulette.min_bet:
                return False

            if all_in is False and (bet > self.roulette.max_bet or bet > cash):
                return False

            if bet > self.roulette.max_bet:
                series.append(bet - self.roulette.max_bet)
                bet = self.roulette.max_bet

            if bet > cash:
                series.append(bet - cash)
                bet = cash # go all in

            cash -= bet
            r = self.roulette.bet_on_color(bet)
            cash += r

            if r == 0:
                series.append(bet)
            else:
                if len(series) > 2:
                    del series[0]
                    del series[-1]
                else:
                    series = self.init_series

            bet = series[0]+series[-1]

        return True
