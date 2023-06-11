from program.F256 import *


class PolynomialF256:

    coeffs = []

    def __init__(self, coeffs):
        self.coeffs = coeffs

    def set_coeff(self, index, f256):
        while len(self.coeffs) <= index:
            self.coeffs.append(get_zero())
        self.coeffs[index] = f256

    def simplify(self):
        if len(self.coeffs) > 0 and self.coeffs[len(self.coeffs) - 1].equal(get_zero()):
            self.coeffs.pop()
            self.simplify()

    def evaluate(self, f256):
        eval = get_zero()
        for i in range(len(self.coeffs)):
            eval = eval.add(self.coeffs[i].multiply(f256.power(i)))
        return eval

    def get_degree(self):
        self.simplify()
        return len(self.coeffs) - 1

    def get_coeff(self, index):
        if len(self.coeffs) <= index:
            return get_zero()
        return self.coeffs[index]

    def derivate(self):
        derivated = PolynomialF256([get_zero()])

        for i in range(self.get_degree()):
            derivated.set_coeff(i, self.get_coeff(i + 1).multiply_by_integer(i + 1))

        return derivated

    def get_coeff_dominant(self):
        return self.get_coeff(self.get_degree())

    def euclidian_division(self, polynomialF256):
        """Renvoie le tuple :"""
        """Quotient de la division euclidienne du polymome par polynomialF256"""
        """Reste de la division euclidienne du polynome par polynomialF256"""
        quotient = PolynomialF256([])
        reste = self.clone()

        while reste.get_degree() >= polynomialF256.get_degree():
            deg = reste.get_degree() - polynomialF256.get_degree()
            divide = PolynomialF256([])
            divide.set_coeff(deg, get_unit())

            toAdd = divide.clone()

            divide = divide.multiply(polynomialF256)
            divide = divide.multiply_by_f256_element(reste.get_coeff_dominant().divide(divide.get_coeff_dominant()))

            toAdd = toAdd.multiply_by_f256_element(divide.get_coeff_dominant().divide(polynomialF256.get_coeff_dominant()))

            reste = reste.substract(divide)
            quotient = quotient.add(toAdd)

        return quotient, reste

    def clone(self):
        return PolynomialF256(self.coeffs.copy())

    def add(self, polynomialF256):
        ret = PolynomialF256([])
        for i in range(max(self.get_degree(), polynomialF256.get_degree()) + 1):
            ret.set_coeff(i, self.get_coeff(i).add(polynomialF256.get_coeff(i)))
        return ret

    def substract(self, polynomialF256):
        ret = PolynomialF256([])
        for i in range(max(self.get_degree(), polynomialF256.get_degree()) + 1):
            ret.set_coeff(i, self.get_coeff(i).substract(polynomialF256.get_coeff(i)))
        return ret

    def multiply(self, polynomialF256):
        ret = PolynomialF256([])
        for k in range(self.get_degree() + polynomialF256.get_degree() + 1):
            somme = get_zero()
            for i in range(k + 1):
                somme = somme.add(self.get_coeff(i).multiply(polynomialF256.get_coeff(k - i)))
            ret.set_coeff(k, somme)
        return ret

    def multiply_by_f256_element(self, f256):
        ret = PolynomialF256([])
        for i in range(self.get_degree() + 1):
            ret.set_coeff(i, self.get_coeff(i).multiply(f256))
        return ret

    def equal(self, polynomialF256):
        if self.get_degree() != polynomialF256.get_degree():
            return False

        for i in range(polynomialF256.get_degree() + 1):
            if not self.get_coeff(i).equal(polynomialF256.get_coeff(i)):
                return False

        return True

    def __str__(self):
        string = ""
        for i in range(len(self.coeffs)):
            coeff = self.get_coeff(i)
            if not coeff.is_zero():
                string += " + (α^" + str(coeff.get_element_alpha_power()) + ")" + ("X^" + str(i) if i != 0 else "") + " "
        return string
