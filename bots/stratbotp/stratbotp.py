#!/usr/bin/env python
"""
Bot that uses propositional logic and fuzzy logic in phase 1 to determine optimal moves according to a predetermined strategy.
Plays passively when leading tricks in phase 1.
Applies minimax with alphabeta pruning in phase 2 to play optimally.
"""

import importlib
import random

from api import Deck, State, util

from .kb import KB, Boolean
from .fuzzykb import fuzzyKB

from . import load as loadfile

class Bot:

    def __init__(self):
        pass

    def alphabeta_value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
        """Returns the value and associated move for a given state

        Args:
            state (State): Current state.
            alpha (float, optional): The highest score that the maximizing player can guarantee given current knowledge. Defaults to float('-inf').
            beta (float, optional): The highest score that the maximizing player can guarantee given current knowledge. Defaults to float('inf').
            depth (int, optional): Our current depth within search tree. Defaults to 0.

        Returns:
            tuple: Best value and move according to minimax
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == 5:
            return heuristic(state)

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        for move in moves:

            next_state = state.next(move)
            value, _ = self.alphabeta_value(next_state)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            if alpha > beta:
                break

        return best_value, best_move
    
    def alphabeta_move(self, state):  # Finds the best move to play next according to the minimax algorithm using alphabeta pruning.
        _, move = self.alphabeta_value(state)
        return move

    def card_fuzzyValue(self, state, index):  # Returns the fuzzy value of a card's fuzzyKB between 0 and 1
        kb = fuzzyKB()

        loadfile.general_information(kb, state, index)
        return kb.fuzzyvalue()
    
    def fuzzy_move(self, state, other_moves):  # returns move with highest fuzzy value
        current_move = other_moves[0]
        highest_fuzzyValue = 0
        for move in other_moves:
            move_fuzzyValue = self.card_fuzzyValue(state, move[0])
            if move_fuzzyValue > highest_fuzzyValue:
                highest_fuzzyValue = move_fuzzyValue
                current_move = move
        return current_move

    def standard_move(self, state, trump_moves, other_moves):
        """Plays non-marriage or non-trump exchange moves according to a specific stratety.
        Passive bot applies its passive strategy if game is in phase 1 and it is leading a trick.
        If game is in phase 2, it calculates the optimal move using minimax with alphabeta pruning.

        Args:
            state (State): Current states
            trump_moves (list): List of moves involving trump cards in hand
            other_moves (list): List of all non-marriage or trump moves

        Returns:
            tuple: Schnapsen move
        """

        if state.get_phase() == 1:
            if state.whose_turn() == state.leader():
                print("Using fuzzyKB")
                return self.fuzzy_move(state, other_moves)
            else:
                opponents_card = state.get_opponents_played_card()
                if is_trump(state, opponents_card):  # if opponent plays a trump card
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
            print("Using alphabeta")
            return self.alphabeta_move(state)

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
            else:  # all remianing moves
                other_moves.append(move)
        
        for move in exchanges:
            if not self.kb_consistent(state, move, "trumpex"):  # tells bot to load 'trump exchange' strategy file as kb
                print("Trump exchange strategy applied")
                return move  # Plays the first move that makes the kb inconsistent

        for move in marriages:
            if not self.kb_consistent(state, move, "marriage"):  # tells bot to load 'marriage' strategy file as kb
                print("Marriage strategy applied")
                return move  # Plays the first move that makes the kb inconsistent
        
        return self.standard_move(state, trump_moves, other_moves)
        
    def kb_consistent(self, state, move, strategy):  # checks KB if move is part of strategy
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

def maximizing(state):  # Whether we are maximizing for player 1 or 2
    return state.whose_turn() == 1

def heuristic(state):  # Returns value between 1.0 and -1.0 of given state according to heuristic evaluating whether player 1 or 2 is better off.
    return util.ratio_points(state, 1) * 2.0 - 1.0, None
    