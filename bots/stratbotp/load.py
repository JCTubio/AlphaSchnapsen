"""
Load file for the fuzzy value of a move
"""
from api import State, util

from .kb import Integer
from .fuzzykb import fuzzyKB, FuzzySymbol

MAX_CARD_POINTS = 11

def general_information(kb, state, index):  # Loads fuzzy symbols, gives them fuzzy values and adds them to fuzzy knowledge base
    RV = FuzzySymbol("rv", set_fuzzyRankValue(state, util.get_rank(index)))  # rank value
    TV = FuzzySymbol("tv", 0.01 if state.get_trump_suit() == util.get_suit(index) else 1)  # trump value
    SV = FuzzySymbol("sv", set_fuzzySuitValue(state, util.get_suit(index)))  # suit value
    
    kb.add_clause(RV)
    kb.add_clause(TV)
    kb.add_clause(SV)

def set_fuzzyRankValue(state, own_rank):  # Returns float between 0 and 1 with how valuable a given card rank is
    points = 1
    if own_rank == 'J':
        points = 2
    elif own_rank == 'Q':
        points = 3
    elif own_rank == 'K':
        points = 4
    elif own_rank == '10':
        points = 10
    else:
        points = 11
    return 1 - (points / MAX_CARD_POINTS)

def set_fuzzySuitValue(state, own_suit):  # Returns float between 0 and 1 with how common a given card suit is in hand
    clubs_count = 0
    diamonds_count = 0
    hearts_count = 0
    spades_count = 0
    
    for card in state.hand():
        if card < 5 : clubs_count += 1
        elif card < 10 : diamonds_count += 1
        elif card < 15 : hearts_count += 1
        else : spades_count += 1
    
    own_count = 0
    if own_suit == "C" : own_count += clubs_count
    elif own_suit == "D" : own_count += diamonds_count
    elif own_suit == "H" : own_count += hearts_count
    else : own_count += spades_count
    
    return own_count / 5
