from program.PolynomialF256 import *

t = 8


generator = PolynomialF256([get_alpha(), get_unit()])
for i in range(2, 2 * t + 1):
    poly = PolynomialF256([get_element_from_alpha_power(i), get_unit()])
    generator = generator.multiply(poly)


def get_generator():
    return generator


def get_x_2t():
    """Renvoie le polynome 1 * x^2t"""
    poly = PolynomialF256([get_zero()])
    poly.set_coeff(2 * t, get_unit())
    return poly


def get_transmission(polynomialF256):
    """Renvoie le polynôme à transmettre pour envoyer le message contenu dans polynomialF256"""
    x2t = get_x_2t()
    I = polynomialF256.multiply(x2t)
    B = I.euclidian_division(get_generator())[1]
    return I.add(B)


def get_test_polynomial():
    """Renvoie le polynome composé de 239 alpha pour tester le programme"""
    poly = PolynomialF256([get_alpha()])
    for j in range(239):
        poly.set_coeff(j, get_alpha())
    return poly


