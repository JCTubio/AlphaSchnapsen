"""
Strategy load file for the marriage strategy.
"""
from .kb import KB, Boolean

C2 = Boolean('c2')
C3 = Boolean('c3')
C7 = Boolean('c7')
C8 = Boolean('c8')
C12 = Boolean('c12')
C13 = Boolean('c13')
C17 = Boolean('c17')
C18 = Boolean('c18')
PC2 = Boolean('pc2')
PC3 = Boolean('pc3')
PC7 = Boolean('pc7')
PC8 = Boolean('pc8')
PC12 = Boolean('pc12')
PC13 = Boolean('pc13')
PC17 = Boolean('pc17')
PC18 = Boolean('pc18')

def general_information(kb):
    """Adds information to knowledge base which cards are kings and queens.

    Args:
        kb (KB): Knowledge base object
    """

    kb.add_clause(C2)
    kb.add_clause(C3)
    kb.add_clause(C7)
    kb.add_clause(C8)
    kb.add_clause(C12)
    kb.add_clause(C13)
    kb.add_clause(C17)
    kb.add_clause(C18)

def strategy_knowledge(kb):
    """Defines the strategy in terms of knowledge base clauses in CNF.
    C(King) ^ C(Queen) <-> PC(Queen) for all four card suits, rewritten in CNF.

    Args:
        kb (KB): Knowledge base object
    """

    kb.add_clause(~PC3, C2)
    kb.add_clause(~PC3, C3)
    kb.add_clause(~C2, ~C3, PC3) # clubs marriage to CNF

    kb.add_clause(~PC8, C7)
    kb.add_clause(~PC8, C8)
    kb.add_clause(~C7, ~C8, PC8) # diamonds marriage to CNF

    kb.add_clause(~PC13, C12)
    kb.add_clause(~PC13, C13)
    kb.add_clause(~C12, ~C13, PC13) # hearts marriage to CNF

    kb.add_clause(~PC18, C18)
    kb.add_clause(~PC18, C18)
    kb.add_clause(~C17, ~C18, PC18) # spades marriage to CNF
