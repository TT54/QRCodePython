class PolynomialF2:
    """Polynome à coefficient dans le corps fini F2\n
    Les éléments de F2 sont représentés par des booléens.\n
    L'addition est le xOR, la multiplication est le AND"""
    coeffs = []

    def __init__(self, coeffs):
        """Initialisation du polynome à partir d'une liste de booléens"""
        self.coeffs = coeffs

    def set_coeff(self, index, coeff):
        """Modifie le coefficient d'indice index"""
        while len(self.coeffs) <= index:
            self.coeffs.append(False)
        self.coeffs[index] = coeff

    def simplify(self):
        """Simplifie l'expression du polynome en retirant tous les coeffs inutiles de la liste"""
        if len(self.coeffs) > 0 and not self.coeffs[len(self.coeffs) - 1]:
            self.coeffs.pop()
            self.simplify()

    def get_coeff(self, index):
        """Renvoie le coefficient d'indice index"""
        return self.coeffs[index] if index < len(self.coeffs) else False

    def get_degree(self):
        """Renvoie le degré du polynome"""
        self.simplify()
        return len(self.coeffs) - 1

    def get_coeff_dominant(self):
        """Renvoie le coefficient dominant du polynome"""
        return self.coeffs[self.get_degree()]

    def multiply(self, p2):
        """Renvoie le résultat de la multiplication par p2"""
        ret = PolynomialF2([])
        for k in range(self.get_degree() + p2.get_degree() + 1):
            somme = False
            for i in range(k + 1):
                somme = somme != (self.get_coeff(i) and p2.get_coeff(k - i))
            ret.set_coeff(k, somme)
        return ret

    def substract(self, p2):
        """Renvoie le résultat de la soustraction par p2"""
        ret = PolynomialF2([])
        for i in range(max(self.get_degree(), p2.get_degree()) + 1):
            ret.set_coeff(i, self.get_coeff(i) != p2.get_coeff(i))
        return ret

    def add(self, p2):
        """Renvoie le résultat de l'ajout de p2"""
        ret = PolynomialF2([])
        for i in range(max(self.get_degree(), p2.get_degree()) + 1):
            ret.set_coeff(i, self.get_coeff(i) != p2.get_coeff(i))
        return ret

    def euclidian_division(self, p2):
        """Renvoie le tuple :\n
        Quotient de la division euclidienne du polymome par p2\n
        Reste de la division euclidienne du polynome par p2"""
        quotient = PolynomialF2([])
        reste = self.clone()

        while reste.get_degree() >= p2.get_degree():
            deg = reste.get_degree() - p2.get_degree()

            divide = PolynomialF2([])
            divide.set_coeff(deg, True)

            toAdd = divide.clone()
            divide = divide.multiply(p2)

            reste = reste.substract(divide)
            quotient = quotient.add(toAdd)

        return quotient, reste

    def euclidian_multiplication(self, p2, modulo):
        """Renvoie le résultat de la multiplication par p2 modulo un certain polynome"""
        return self.multiply(p2).euclidian_division(modulo)

    def clone(self):
        """Renvoie une copie du polynome"""
        return PolynomialF2(self.coeffs.copy())

    def __hash__(self):
        somme = 0
        for i in range(len(self.coeffs)):
            somme += 2 ** i if self.get_coeff(i) else 0
        return somme

    def __str__(self):
        string = ""
        for i in range(len(self.coeffs)):
            coeff = 1 if self.coeffs[i] else 0
            if coeff != 0:
                string += " + " + str(coeff) + ("X^" + str(i) if i != 0 else "") + " "
        return string

    def equal(self, p2):
        """Renvoie si les deux polynomes sont égaux"""
        if p2.get_degree() != self.get_degree():
            return False

        for i in range(self.get_degree() + 1):
            if self.get_coeff(i) != p2.get_coeff(i):
                return False

        return True
