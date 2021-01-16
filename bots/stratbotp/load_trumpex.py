'''Initialising all variables needed for trump-exchange strategy'''
from .kb import KB, Boolean, Integer

# C0 = Boolean('c0')
# C1 = Boolean('c1')
# C2 = Boolean('c2')
# C3 = Boolean('c3')
C4 = Boolean('c4')
# C5 = Boolean('c5')
# C6 = Boolean('c6')
# C7 = Boolean('c7')
# C8 = Boolean('c8')
C9 = Boolean('c9')
# C10 = Boolean('c10')
# C11 = Boolean('c11')
# C12 = Boolean('c12')
# C13 = Boolean('c13')
C14 = Boolean('c14')
# C15 = Boolean('c15')
# C16 = Boolean('c16')
# C17 = Boolean('c17')
# C18 = Boolean('c18')
C19 = Boolean('c19')
# PC0 = Boolean('pc0')
# PC1 = Boolean('pc1')
# PC2 = Boolean('pc2')
# PC3 = Boolean('pc3')
PC4 = Boolean('pc4')
# PC5 = Boolean('pc5')
# PC6 = Boolean('pc6')
# PC7 = Boolean('pc7')
# PC8 = Boolean('pc8')
PC9 = Boolean('pc9')
# PC10 = Boolean('pc10')
# PC11 = Boolean('pc11')
# PC12 = Boolean('pc12')
# PC13 = Boolean('pc13')
PC14 = Boolean('pc14')
# PC15 = Boolean('pc15')
# PC16 = Boolean('pc16')
# PC17 = Boolean('pc17')
# PC18 = Boolean('pc18')
PC19 = Boolean('pc19')

def general_information(kb):
    # GENERAL INFORMATION ABOUT THE CARDS
    # This adds information which cards are Jacks
    kb.add_clause(C4)
    kb.add_clause(C9)
    kb.add_clause(C14)
    kb.add_clause(C19)

def strategy_knowledge(kb):
    # DEFINITION OF THE STRATEGY
    # for all indexes x PC(x) <-> C(x), converted to CNF
    kb.add_clause(~C4, PC4)
    kb.add_clause(~PC4, C4)
    kb.add_clause(~C9, PC9)
    kb.add_clause(~PC9, C9)
    kb.add_clause(~C14, PC14)
    kb.add_clause(~PC14, C14)
    kb.add_clause(~C19, PC19)
    kb.add_clause(~PC19, C19)
    
