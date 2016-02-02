__author__ = 'chachalaca'

class Strategy:

    init_bet = None
    cash = None
    roulette = None

    @staticmethod
    def get_name(self):
        return self.__class__.__name__

    def play(self):
        pass

    def play_for(self, goal, all_in=True):
        pass
