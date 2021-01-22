import sys

class Symbol(object):
    """
    A class representing a single unit in the fuzzy KB.
    """
    pass

class FuzzySymbol(Symbol):

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def name(self):
        return self.__name

    def value(self):
        return self.__value

    def __invert__(self):
        # type: () -> Boolean
        """
        :return:
        """
        return _NegFuzzySymbol(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name() == other.name()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name())

    def __repr__(self):
        return self.name()

class _NegFuzzySymbol(FuzzySymbol):

    def __init__(self, symbol):
        self.__symbol = symbol

    def name(self):
        return self.__symbol.name()

    def value(self):
        value = self.__symbol.value()
        # Here you will have to determine the fuzzy value of a negated symbol
        return 1 - value

    def __invert__(self):
        return self.__symbol

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name() == other.name()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name(), False)

    def __repr__(self):
        return '~' + self.name()

class fuzzyKB(object):
    """
    A class representing a fuzzy knowledge base.
    """

    def __init__(self):
        self._symbols = []
        self._clauses = []

    def add_clause(self, *symbols):
        """
        Adds a fuzzy clause. A clause is a disjunction of atomic symbols or their negations.
        ```
            A = FuzzySymbol('A')
            B = FuzzySymbol('B')
            C = FuzzySymbol('C')

            kb = fuzzyKB()
            kb.add_clause(A, B, ~C) # A or B or not C
            kb.add_clause(A, ~B)    # A or not B
        ```

        :param symbols:
        :return:
        """

        clause = list(symbols)

        # Check the types of the input
        for elem in clause:
            if not (isinstance(elem, FuzzySymbol)):
                raise ValueError('Only FuzzySymbols can be part of clauses. Encountered {} of type {}'.format(elem, elem.__class__))

        index = len(self._clauses)
        self._clauses.append(clause)

        for symbol in symbols:
            raw_symbol = ~symbol if isinstance(symbol, _NegFuzzySymbol) else symbol

            if raw_symbol not in self._symbols:
                self._symbols.append(raw_symbol)


    def fuzzyvalue(self):
        """
        :return: The fuzzy value of a clause set. Remember that a clause corresponds to a disjunction and
        a set of clauses to a conjunction of formulas. You will need this to finish the implementation.
        Use pythons min and max functions for lists to calculate
        """
        minvalue = []
        for clause in self._clauses:
            clausevalue = []
            for symbol in clause:
                clausevalue.append(symbol.value())
            minvalue.append(max(clausevalue))
        return min(minvalue)

