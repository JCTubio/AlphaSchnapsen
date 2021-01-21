#!/usr/bin/env python
"""
This is a bot that applies propositional logic reasoning to determine its strategy.
The strategy it uses is determined by what is defined in load.py.

It loads general information about the game, as well as the definition of a strategy,
from load.py.
"""

import importlib
import random

from api import Deck, State, util

from .kb import KB, Boolean, Integer
from .fuzzykb import fuzzyKB

from . import load as loadfile

class Bot:

    def __init__(self):
        pass

    def card_fuzzyValue(self, state, index):  # returns fuzzy value of given card index
        kb = fuzzyKB()

        loadfile.general_information(kb, state, index)
        return kb.fuzzyvalue()
    
    def fuzzy_move(self, state, other_moves):  # returns move with highest fuzzy value
        current_move = other_moves[0]
        highest_fuzzyValue = 0
        for move in other_moves:
            move_fuzzyValue = self.card_fuzzyValue(state, move[0])
            print(f"FuzzyValue of move {util.get_card_name(move[0])} = {move_fuzzyValue}")
            if move_fuzzyValue > highest_fuzzyValue:
                highest_fuzzyValue = move_fuzzyValue
                current_move = move
        print(f"Selected highest: {highest_fuzzyValue}")
        return current_move

    def standard_move(self, state, trump_moves, other_moves):
        if state.get_phase() == 1:
            if state.whose_turn() == state.leader():
                return self.fuzzy_move(state, other_moves)
            else:
                opponents_card = state.get_opponents_played_card()
                if is_trump(state, opponents_card):
                    print("Played lowest ranking move")
                    return lowest_rank_move(other_moves)
                elif opponents_card % 5 <= 1:  # if opponent plays ace or 10
                    if len(trump_moves) > 0:
                        print("Played lowest owned trump")
                        return lowest_rank_move(trump_moves)  # win trick using trump to gain many points
                    else:
                        print("Played lowest ranking move")
                        return lowest_rank_move(other_moves)
                else:  # if opponent plays jack, queen or king
                    print("Played lowest winning move")
                    return lowest_winning_move(other_moves, opponents_card)
        else:  # phase 2
            return "nope"

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
            else:
                other_moves.append(move)
        
        for move in exchanges:
            if not self.kb_consistent(state, move, "trumpex"):  # tells bot to load 'trump exchange' strategy file as kb
                print("Trump exchange strategy applied")
                return move  # Plays the first move that makes the kb inconsistent

        for move in marriages:
            if not self.kb_consistent(state, move, "marriage"):  # tells bot to load 'marriage' strategy file as kb
                print("Marriage strategy applied")
                return move  # Plays the first move that makes the kb inconsistent
        
        std_move = self.standard_move(state, trump_moves, other_moves)
        return std_move if std_move != "nope" else self.fuzzy_move(state, other_moves + trump_moves)  # temporary while phase 2 not implemented yet
        
        # return self.fuzzy_move(state, other_moves + trump_moves)  # return the move decided by fuzzy passive strategy

    def kb_consistent(self, state, move, strategy):  # checks non-fuzzy KB if move is part of strategy
        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # load strategy file
        path = f"bots.stratbotp.load_{strategy}"
        try:
            load = importlib.import_module(path)
        except:
            print(f"ERROR: Could not load the python file {path}")

        load.general_information(kb)
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[1] if strategy == "trumpex" else move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        variable_string = "pc" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()
    
def is_trump(state, move):
    return util.get_suit(move) == state.get_trump_suit() if move is not None else "None move"

def lowest_rank_move(moves):
    lowest_move = moves[0]
    for move in moves:
        if lowest_move[0] % 5 <= move[0] % 5:
            lowest_move = move
    return lowest_move

def lowest_winning_move(moves, opponents_card):
    """Returns the lowest ranking card that wins current trick against the card the opponent has played.
    If not possible, returns the lowest ranking card in hand.

    Args:
        moves (list): List of moves to choose from
        opponents_card (int): Index of card that opponent has played

    Returns:
        tuple: Schnapsen move
    """
    higher_same_suit = []  # possible moves that are higher rank and same suit as opponent's card
    for move in moves:
        if util.get_suit(move[0]) == util.get_suit(opponents_card) and move[0] % 5 < opponents_card % 5:
            higher_same_suit.append(move)

    if len(higher_same_suit) > 0:
        return lowest_rank_move(higher_same_suit)
    else:
        return lowest_rank_move(moves)
