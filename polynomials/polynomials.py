from numbers import Number


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a - b for a, b in zip(self.coefficients,
                                                other.coefficients))
            if self.degree() < other.degree():
                coefs += tuple(-c for c in other.coefficients[common:])
            else:
                coefs += self.coefficients[common:]
            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented
    
    def __rsub__(self, other):
        return Polynomial(tuple(-c for c in self.coefficients)) + other

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            coefs = Polynomial(tuple(self.coefficients[0]*a for a in other.coefficients))
            zeros = (0,)
            for i in range(self.degree()):
                coefs += Polynomial(zeros + tuple(self.coefficients[i+1]*a for a in other.coefficients))
                zeros += (0,)
            return coefs

        elif isinstance(other, Number):
            return Polynomial(tuple(other*a for a in self.coefficients))

        else:
            return NotImplemented
    
    def __rmul__(self, other):
        return self*other
    
    def __pow__(self, other):
        exp = 1
        for i in range(other):
            exp = exp*self
        
        return exp

    def __call__(self, other):
        total = 0
        for i in range(self.degree()+1):
            total += self.coefficients[i]*(other**i)
        
        return total

    def dx(self):
        derivative = tuple(a*b for a, b in enumerate(self.coefficients))
        if self.degree() == 0:
            return Polynomial(derivative)
        else:
            return Polynomial(derivative[1:len(derivative)])

def derivative(polynomial):
    return polynomial.dx()
