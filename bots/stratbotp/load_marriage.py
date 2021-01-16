'''Initialising all variables needed for marriage strategy'''
from .kb import KB, Boolean, Integer

# C0 = Boolean('c0')
# C1 = Boolean('c1')
C2 = Boolean('c2')
C3 = Boolean('c3')
# C4 = Boolean('c4')
# C5 = Boolean('c5')
# C6 = Boolean('c6')
C7 = Boolean('c7')
C8 = Boolean('c8')
# C9 = Boolean('c9')
# C10 = Boolean('c10')
# C11 = Boolean('c11')
C12 = Boolean('c12')
C13 = Boolean('c13')
# C14 = Boolean('c14')
# C15 = Boolean('c15')
# C16 = Boolean('c16')
C17 = Boolean('c17')
C18 = Boolean('c18')
# C19 = Boolean('c19')
# PC0 = Boolean('pc0')
# PC1 = Boolean('pc1')
PC2 = Boolean('pc2')
PC3 = Boolean('pc3')
# PC4 = Boolean('pc4')
# PC5 = Boolean('pc5')
# PC6 = Boolean('pc6')
PC7 = Boolean('pc7')
PC8 = Boolean('pc8')
# PC9 = Boolean('pc9')
# PC10 = Boolean('pc10')
# PC11 = Boolean('pc11')
PC12 = Boolean('pc12')
PC13 = Boolean('pc13')
# PC14 = Boolean('pc14')
# PC15 = Boolean('pc15')
# PC16 = Boolean('pc16')
PC17 = Boolean('pc17')
PC18 = Boolean('pc18')
# PC19 = Boolean('pc19')

def general_information(kb):
    # GENERAL INFORMATION ABOUT THE CARDS
    # This adds information which cards are Queens and Kings
    kb.add_clause(C2)
    kb.add_clause(C3)
    kb.add_clause(C7)
    kb.add_clause(C8)
    kb.add_clause(C12)
    kb.add_clause(C13)
    kb.add_clause(C17)
    kb.add_clause(C18)

def strategy_knowledge(kb):
    # DEFINITION OF THE STRATEGY
    # for all cards C: (C(king) ^ C(queen) <-> PC(King)) converted to CNF
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
