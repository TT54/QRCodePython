from program.PolynomialF2 import *

ideal = PolynomialF2([True, False, True, True, True, False, False, False, True])


class F256:
    """Element de F256 (immuable)"""
    position = 0
    polynomial = PolynomialF2([])

    def __init__(self, position, polynomial):
        """Initialisation d'un élément de F256 avec son indice et son polynome dans F2[X] associé\n
        Attention : Ce constructeur ne doit pas être utilisé en dehors de cette classe !"""
        self.polynomial = polynomial
        self.position = position

    def get_polynomial(self):
        """Renvoie le polynome à coeffs dans F2 associé"""
        return self.polynomial

    def brutal_multiplication(self, f256):
        """Renvoie le résultat de la multiplication par f256 en passant par les polynomes"""
        return get_element_with_polynomial(self.polynomial.euclidian_multiplication(f256.polynomial, ideal)[1])

    def get_element_alpha_power(self):
        """Renvoie la puissance d'alpha de cet élément"""
        return get_alpha_power(self)

    def get_element_inverse(self):
        """Renvoie l'inverse par la multiplication"""
        return get_inverse(self)

    def is_zero(self):
        """Renvoie s'il s'agit du zéro"""
        return self.position == 0

    def multiply(self, f256):
        """Renvoie le résultat de la multiplication par f256"""
        if self.is_zero() or f256.is_zero():
            return get_zero()

        other_power = f256.get_element_alpha_power()
        new_power = (self.get_element_alpha_power() + other_power) % 255

        return get_element_from_alpha_power(new_power)

    def add(self, f256):
        """Renvoie le résultat de l'ajout de f256"""
        return get_element_with_polynomial(self.polynomial.add(f256.polynomial))

    def substract(self, f256):
        """Renvoie le résultat de la soustraction de f256"""
        return get_element_with_polynomial(self.polynomial.substract(f256.polynomial))

    def power(self, i):
        """Renvoie l'élément mis à la puissance i"""
        f256 = get_unit()
        for i in range(i):
            f256 = f256.multiply(self)
        return f256

    def multiply_by_integer(self, i):
        """Renvoie le résultat de la multiplication par un entier"""
        result = get_zero()
        for i in range(i):
            result = result.add(self)
        return result

    def divide(self, f256):
        """Renvoie le résultat de la division par f256"""
        return self.multiply(f256.get_element_inverse())

    def equal(self, f256):
        """Renvoie si les deux éléments de F256 sont égaux"""
        return self.polynomial.equal(f256.polynomial)

    def __hash__(self):
        return self.polynomial.__hash__()

    def __str__(self):
        string = ""
        for i in range(self.polynomial.get_degree(), -1, -1):
            coeff = 1 if self.polynomial.get_coeff(i) else 0
            if coeff != 0:
                string += " + " + str(coeff) + ("α^" + str(i) if i != 0 else "") + " "
        return "0" if string == "" else string


elements_poly = {}
inverses = {}
alpha_powers = {}
element_from_alpha_powers = {}

elements = [None for i in range(256)]


def get_reverse_binary_from_byte(byte):
    """Renvoie une liste de bits (booleans) associés à un octet"""
    converted = [False] * 8
    range = 0
    while byte >= 1:
        r = byte % 2
        converted[range] = r == 1
        range += 1
        byte = byte // 2
    return converted


def generate_elements():
    """Permet de générer les éléments de F256"""
    for i in range(256):
        pol = PolynomialF2(get_reverse_binary_from_byte(i))
        hash_code = pol.__hash__()
        f256 = F256(hash_code, pol)
        elements[hash_code] = f256


def generate_inverses():
    """Permet de générer tous les inverses de F256"""
    unit = get_unit()
    for i in range(256):
        for j in range(256):
            if elements[i].brutal_multiplication(elements[j]).equal(unit):
                inverses[elements[i]] = elements[j]
                inverses[elements[j]] = elements[i]


def generate_alpha_powers():
    """Permet de calculer toutes les puissances de alpha dans F256"""
    alpha = get_alpha()
    calcul = get_unit()
    for i in range(255):
        alpha_powers[calcul] = i
        element_from_alpha_powers[i] = calcul
        calcul = calcul.brutal_multiplication(alpha)


def get_element(index):
    """Renvoie l'élément indexé par index"""
    return elements[index]


def get_element_with_polynomial(p):
    """Renvoie l'élément associé au polynome p"""
    return elements[p.__hash__()]


def get_unit():
    """Renvoie l'élément unitaire (neutre par multiplication) de F256"""
    return get_element_with_polynomial(PolynomialF2([True]))


def get_alpha():
    """Renvoie alpha"""
    return get_element_with_polynomial(PolynomialF2([False, True]))


def get_zero():
    """Renvoie le nul (neutre de l'addition)"""
    return get_element_with_polynomial(PolynomialF2([False]))


def get_inverse(f256):
    """Renvoie l'inverse d'un élément"""
    return inverses[f256]


def get_alpha_power(f256):
    """Renvoie la puissance d'alpha d'un élément"""
    return alpha_powers[f256]


def get_element_from_alpha_power(power):
    """Renvoie l'élément depuis une puissance d'alpha"""
    return element_from_alpha_powers[power]


generate_elements()
generate_inverses()
generate_alpha_powers()
