from program.Encoder import *
from program.Decoder import *


def test():
    to_send = get_transmission(get_test_polynomial())
    initial = to_send.clone()

    to_send.set_coeff(0, get_element(8))
    to_send.set_coeff(3, get_element(135))
    to_send.set_coeff(4, get_element(12))

    decoded = correction(to_send)

    print(decoded.equal(initial))


