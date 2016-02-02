__author__ = 'chachalaca'

import numpy as np

from FrenchRoulette import FrenchRoulette
from AmericanRoulette import AmericanRoulette
from Martingale import Martingale
from Fibonacci import Fibonacci
from DAlembert import DAlembert
from Labouchere import Labouchere
from AntiMartingale import AntiMartingale

import pandas as pd
import seaborn as sns

sns.set(style="darkgrid")

iterations = 10000

init_bet = 1
min_bet = 1
max_bet = 50
cash = 100

roulettes = [
    FrenchRoulette,
    AmericanRoulette
]
strategies = [
    Martingale,
    Fibonacci,
    DAlembert,
    Labouchere,
    AntiMartingale
]

param_str = str(init_bet)+"-"+str(min_bet)+"-"+str(max_bet)+"-"+str(cash)
param_str_short = str(init_bet)+"-"+str(min_bet)


def main():

    run_simulations()
    make_visualizations()
    print_stats()


def run_simulations():

    avg = {}
    data = pd.DataFrame(columns=('roulette', 'strategy', 'rounds', 'max_cash', 'doubled'))
    data2 = pd.DataFrame(columns=('roulette', 'strategy', 'max_bet', 'cash', 'doubled', 'all_in'))

    for Roulette in roulettes:
        avg[Roulette.__name__] = {}
        print(Roulette.__name__)

        for Strategy in strategies:
            print(Strategy.__name__)

            # General simulations

            for game in range(1, iterations):
                strategy = Strategy(init_bet, cash, Roulette(min_bet, max_bet))
                result = strategy.play()
                double = strategy.play_for(cash*2)

                data.loc[len(data)+1] = [
                    Roulette.__name__,
                    Strategy.__name__,
                    len(result),
                    max(list(map(lambda r: r["cash"], result))),
                    double
                ]

            # Probability data for heatmaps

            r = [min_bet*i for i in range(1,20)] # range for max_bet & cash values

            for max_bet_value in r:

                for cash_value in r:

                    doubled = []
                    doubled_all_in = []

                    for game in range(1, 500):
                        strategy = Strategy(init_bet, cash_value, Roulette(min_bet, max_bet_value))
                        doubled.append(strategy.play_for(goal=cash_value*2, all_in=False))
                        doubled_all_in.append(strategy.play_for(goal=cash_value*2, all_in=True))

                    data2.loc[len(data2)+1] = [
                        Roulette.__name__,
                        Strategy.__name__,
                        str(int(max_bet_value)),
                        str(int(cash_value)),
                        np.average(doubled),
                        False
                    ]
                    data2.loc[len(data2)+1] = [
                        Roulette.__name__,
                        Strategy.__name__,
                        max_bet_value,
                        cash_value,
                        np.average(doubled_all_in),
                        True
                    ]

    data.to_pickle("data/data-"+param_str+".pkl")
    data2.to_pickle("data/data2-"+param_str_short+".pkl")

    # data.to_csv("data/data-"+param_str+".csv")


def make_visualizations():

    data = pd.read_pickle("data/data-"+param_str+".pkl")
    data2 = pd.read_pickle("data/data2-"+param_str_short+".pkl")

    data2[["max_bet", "cash"]] = data2[["max_bet", "cash"]].astype(int)

    for Roulette in roulettes:
        for Strategy in strategies:

            filtered1 = data[data["roulette"] == Roulette.__name__]
            filtered = filtered1[filtered1["strategy"] == Strategy.__name__]

            print(filtered.count())

            # Individual distribution plots

            sns.distplot(filtered["rounds"].tolist())
            sns.plt.savefig("figures/"+Roulette.__name__+Strategy.__name__+"-"+param_str+"-rounds.png")
            sns.plt.clf()

            sns.distplot(filtered["max_cash"].tolist())
            sns.plt.savefig("figures/"+Roulette.__name__+Strategy.__name__+"-"+param_str+"-max_cash.png")
            sns.plt.clf()

    # Distribution plots

    g = sns.FacetGrid(data, row="strategy", col="roulette", margin_titles=True, size=3, aspect=1)
    g.map(sns.kdeplot, "max_cash", shade=True, cut=0)
    g.set(xlim=(cash, 400), ylim=(0, 0.04))
    g.savefig("figures/strategies/max_cash-"+param_str_short+".png")

    g = sns.FacetGrid(data, row="strategy", col="roulette", margin_titles=True, size=3, aspect=1)
    g.map(sns.kdeplot, "rounds", shade=True, cut=0)
    g.set(xlim=(0, 1000), ylim=(0, 0.04))
    g.savefig("figures/strategies/rounds-"+param_str_short+".png")

    # Probability heatmaps

    g = sns.FacetGrid(data2[data2["all_in"] == 1], row="strategy", col="roulette", margin_titles=True, size=5, aspect=1)
    g.map_dataframe(lambda data, color: sns.heatmap(data.pivot('max_bet', 'cash', 'doubled'), linewidths=.5, vmin=0, vmax=1))
    g.savefig("figures/probabilities/heatmap-all_in-"+param_str_short+".png")

    g = sns.FacetGrid(data2[data2["all_in"] == 0], row="strategy", col="roulette", margin_titles=True, size=5, aspect=1)
    g.map_dataframe(lambda data, color: sns.heatmap(data.pivot('max_bet', 'cash', 'doubled'), linewidths=.5, vmin=0, vmax=1))
    g.savefig("figures/probabilities/heatmap-"+param_str_short+".png")


def print_stats():

    data = pd.read_pickle("data/data-"+param_str+".pkl")

    avg = {}
    for Roulette in roulettes:
        avg[Roulette.__name__] = {}

        for Strategy in strategies:

            filtered1 = data[data["roulette"] == Roulette.__name__]
            filtered = filtered1[filtered1["strategy"] == Strategy.__name__]

            avg[Roulette.__name__][Strategy.__name__] = {
                "rounds": str(np.average(filtered["rounds"].tolist()))+" ("+str(np.var(filtered["rounds"].tolist()))+")",
                "maximum cash": str(np.average(filtered["max_cash"].tolist()))+" ("+str(np.var(filtered["max_cash"].tolist()))+")",
                "double cash probability": str(np.average(filtered["doubled"].tolist()))
            }

    __pretty_print_dict(avg)


def __pretty_print_dict(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         __pretty_print_dict(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))


if __name__ == "__main__":
    main()
