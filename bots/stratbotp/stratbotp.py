#!/usr/bin/env python
"""
This is a bot that applies propositional logic reasoning to determine its strategy.
The strategy it uses is determined by what is defined in load.py.

It loads general information about the game, as well as the definition of a strategy,
from load.py.
"""

import random
import importlib

from api import Deck, State, util

# from . import load
from .kb import KB, Boolean, Integer

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        moves = state.moves()
        exchanges = []
        marriages = []
        trump_moves = []
        other_moves = []

        random.shuffle(moves)

        for move in moves:
            if move[0] is None:  # trump exchange
                exchanges.append(move)
            elif move[1] is not None:  # marriage
                marriages.append(move)
            elif is_trump(state, move[0]):  # move involving a trump card
                trump_moves.append(move)
            # else:
            #     other_moves.append(move)

        for move in exchanges:
            if not self.kb_consistent(state, move, "trumpex"):  # tells bot to load 'trump exchange' strategy file as kb
                print("Trump exchange strategy applied")
                return move  # Plays the first move that makes the kb inconsistent

        for move in marriages:
            if not self.kb_consistent(state, move, "marriage"):  # tells bot to load 'marriage' strategy file as kb
                print("Marriage strategy applied")
                return move  # Plays the first move that makes the kb inconsistent
        
        # # TEMPORARY
        # chosen_move = moves[0]
        # # If the opponent has played a card
        # if state.get_opponents_played_card() is not None:
        #     moves_same_suit = []

        #     # Get all moves of the same suit as the opponent's played card
        #     for index, move in enumerate(moves):
        #         if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card()):
        #             moves_same_suit.append(move)

        #     if len(moves_same_suit) > 0:
        #         chosen_move = moves_same_suit[0]
        #         return chosen_move

        # # Get move with highest rank available, of any suit
        # for index, move in enumerate(moves):
        #     if move[0] is not None and move[0] % 5 <= chosen_move[0] % 5:
        #         chosen_move = move
        # return chosen_move
        # # TEMPORARY

        # If no move that is entailed by the kb is found, play random move
        return random.choice(moves)

    # Note: In this example, the state object is not used,
    # but you might want to do it for your own strategy.
    def kb_consistent(self, state, move, strategy):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # load strategy file
        path = f"bots.stratbotp.load_{strategy}"
        # try:
        #     load = importlib.import_module(load_filename)
        # except:
        #     print(f"ERROR: Could not load the python file {load_filename}")
        #     # traceback.print_exc()
        #     # sys.exit(1)
        load = importlib.import_module(path)
   
        # Add general information about the game
        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if 
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pc" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()

def is_trump(state, move):
    trump_suit = state.get_trump_suit()
    move_suit = util.get_suit(move)
    return trump_suit == move_suit
