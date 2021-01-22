"""
Load file for the trump exchange strategy.
"""
from .kb import KB, Boolean

C4 = Boolean('c4')
C9 = Boolean('c9')
C14 = Boolean('c14')
C19 = Boolean('c19')
PC4 = Boolean('pc4')
PC9 = Boolean('pc9')
PC14 = Boolean('pc14')
PC19 = Boolean('pc19')

def general_information(kb):
    """Adds information to knowledge base which cards are jacks.

    Args:
        kb (KB): Knowledge base object
    """

    kb.add_clause(C4)
    kb.add_clause(C9)
    kb.add_clause(C14)
    kb.add_clause(C19)

def strategy_knowledge(kb):
    """Defines the strategy in terms of knowledge base clauses in CNF.
    C(Jack) <-> PC(Jack) for all four card suits, rewritten in CNF.

    Args:
        kb (KB): Knowledge base object
    """

    kb.add_clause(~C4, PC4)
    kb.add_clause(~PC4, C4)
    kb.add_clause(~C9, PC9)
    kb.add_clause(~PC9, C9)
    kb.add_clause(~C14, PC14)
    kb.add_clause(~PC14, C14)
    kb.add_clause(~C19, PC19)
    kb.add_clause(~PC19, C19)
    
