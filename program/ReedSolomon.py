from program.Encoder import *
from program.Decoder import *


def test():
    to_send = get_transmission(get_test_polynomial())
    initial = to_send.clone()

    to_send.set_coeff(0, get_element(8))
    to_send.set_coeff(3, get_element(135))
    to_send.set_coeff(4, get_element(12))

    decoded = get_correction(to_send)

    print(decoded.equal(initial))


def encode(message):
    """Prend en argument un polynome dans F256[X] et renvoie le message à transmettre"""
    return get_transmission(message)


def decode(received):
    """Prend en argument un polynome dans F256[X] et renvoie le message à décodé"""
    return get_correction(received)


def get_F256_from_byte(byte):
    """Renvoie l'élément de F256 associé à l'octet byte"""
    return get_element_with_polynomial(PolynomialF2(get_reverse_binary_from_byte(byte)))


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


def get_byte_from_F256(f256):
    """Renvoie l'octet associé à un élément de F256"""
    b = 0
    poly = f256.get_polynomial()
    for i in range(poly.get_degree() + 1):
        if poly.get_coeff(i):
            b += 2 ** i
    return b


def get_polynomial_from_bytes(data):
    """Renvoie le polynome associé à une liste d'octets"""
    poly = PolynomialF256([])
    for i in range(len(data)):
        poly.set_coeff(i, get_F256_from_byte(data[i]))
    return poly


def get_bytes_from_polynomial(polynomialF256):
    """Renvoie la liste d'octets associée à un polynome de F256[X]"""
    byte_array = [0] * (polynomialF256.get_degree() + 1)
    for i in range(polynomialF256.get_degree() + 1):
        byte_array[i] = get_byte_from_F256(polynomialF256.get_coeff(i))
    return byte_array


def encode_bytes(data):
    """Renvoie la liste d'octets encodées avec Reed Solomon à partir d'une liste d'octets data"""
    return get_bytes_from_polynomial(encode(get_polynomial_from_bytes(data)))


def decode_bytes(data):
    """Renvoie la liste d'octets décodée avec Reed Solomon à partir d'une liste reçue data"""
    return get_bytes_from_polynomial(decode(get_polynomial_from_bytes(data)))
