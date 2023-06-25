from program.PolynomialF256 import *
from program.Encoder import *


def get_syndrome(polynomialF256):
    """Renvoie le syndrome du polynôme polynomialF256"""
    S = PolynomialF256([get_zero()])
    for i in range(1, 2 * t + 1):
        S.set_coeff(i - 1, polynomialF256.evaluate(get_element_from_alpha_power(i)))
    return S


def get_bezout(poly1, poly2):
    """Effectue l'algorithme d'Euclide étendu pour obtenir une relation de Bézout de la forme"""
    """a * poly1 + b * poly2 = c"""
    """Renvoie alors le triplet (a, b, c)"""

    r0, r1 = poly2, poly1
    u0, u1 = PolynomialF256([get_unit()]), PolynomialF256([get_zero()])
    v0, v1 = PolynomialF256([get_zero()]), PolynomialF256([get_unit()])

    while r1.get_degree() >= t:
        quotient, reste = r0.euclidian_division(r1)

        r0, r1 = r1, reste
        u0, u1 = u1, u0.substract(u1.multiply(quotient))
        v0, v1 = v1, v0.substract(v1.multiply(quotient))

    return v1, u1, r1


def get_correction(polynomialF256):
    """Renvoie le polynôme corrigé obtenu à partir de polynomialF256"""
    syndrome = get_syndrome(polynomialF256)

    if syndrome.equal(PolynomialF256([get_zero()])):
        return polynomialF256

    L, b, w = get_bezout(syndrome, get_x_2t())
    if w.equal(PolynomialF256([get_zero()])):
        return None

    error_positions = []
    for i in range(1, 256):
        eval = L.evaluate(get_element(i))
        if eval.is_zero():
            error_positions.append((256 - get_element(i).get_element_alpha_power() - 1) % 255)

    corrector = PolynomialF256([get_zero()])

    for position in error_positions:
        alpha_i = get_element_from_alpha_power(position)
        corrector.set_coeff(position, w.evaluate(alpha_i.get_element_inverse()).divide(L.derivate().evaluate(alpha_i.get_element_inverse())))

    return polynomialF256.add(corrector)
