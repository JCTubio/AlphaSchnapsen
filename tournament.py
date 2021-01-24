#!usr/bin/env python
"""
A command line program for multiple games between several bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
from api import State, util, engine
import random, time, csv

def run_tournament(options):

    botnames = options.players.split(",")

    bots = []
    for botname in botnames:
        bots.append(util.load_player(botname))

    n = len(bots)
    wins = [0] * len(bots)
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * options.repeats
    playedgames = 0

    totalScores = [[botnames[0], botnames[1], 'winner', 'points', f'{botnames[0]} phase1 score', f'{botnames[1]} phase1 score', f'{botnames[0]} phase2 score', f'{botnames[1]} phase2 score']] # total scores to output to csv

    print('Playing {} games:'.format(int(totalgames)))
    for a, b in matches:
        for r in range(options.repeats):

            if random.choice([True, False]):
                p = [a, b]
            else:
                p = [b, a]

            # Generate a state with a random seed
            state = State.generate(phase=int(options.phase))

            (winner, score), (player1score, player2score), (player1phase1score, player1phase2score, player2phase1score, player2phase2score) = engine.play(bots[p[0]], bots[p[1]], state, options.max_time*1000, verbose=options.verbose, fast=options.fast)

            if winner is not None:
                winner = p[winner - 1]
                wins[winner] += score
                scores = [0, 0, 0, 0, 0, 0, 0, 0] # initial values for total scores
                scores[p[0]] = player1score
                scores[p[1]] = player2score
                scores[2] = botnames[winner]
                scores[3] = score
                scores[p[0] + 4] = player1phase1score
                scores[p[1] + 4] = player2phase1score
                scores[p[0] + 6] = player1phase2score
                scores[p[1] + 6] = player2phase2score
                totalScores.append(scores)

            playedgames += 1
            print(f'Player {bots[p[0]]} scored: {player1score}')
            print(f'Player {bots[p[1]]} scored: {player2score}')
            print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))
            print()
            
    print('Results:')
    for i in range(len(bots)):
        print('    bot {}: {} points'.format(bots[i], wins[i]))

    # output values to csv
    with open('scores.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for totalScore in totalScores:
            wr.writerow(totalScore)

if __name__ == "__main__":

    ## Parse the command line options
    parser = ArgumentParser()

    parser.add_argument("-s", "--starting-phase",
                        dest="phase",
                        help="Which phase the game should start at.",
                        default=1)

    parser.add_argument("-p", "--players",
                        dest="players",
                        help="Comma-separated list of player names (enclose with quotes).",
                        default="rand,bully,rdeep")

    parser.add_argument("-r", "--repeats",
                        dest="repeats",
                        help="How many matches to play for each pair of bots",
                        type=int, default=10)

    parser.add_argument("-t", "--max-time",
                        dest="max_time",
                        help="maximum amount of time allowed per turn in seconds (default: 5)",
                        type=int, default=5)

    parser.add_argument("-f", "--fast",
                        dest="fast",
                        action="store_true",
                        help="This option forgoes the engine's check of whether a bot is able to make a decision in the allotted time, so only use this option if you are sure that your bot is stable.")

    parser.add_argument("-v", "--verbose",
                        dest="verbose",
                        action="store_true",
                        help="Print verbose information")

    options = parser.parse_args()

    run_tournament(options)
