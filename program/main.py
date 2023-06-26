from QrCode import *


generate_qr_code("abcdefghij", 'D:\\Theo\\Cours\\Tipe\\Maths\\image.png')

print(read_qr_code('D:\\Theo\\Cours\\Tipe\\Maths\\image.png'))
print(read_qr_code('D:\\Theo\\Cours\\Tipe\\Maths\\image_modif.png'))
print(read_qr_code('D:\\Theo\\Cours\\Tipe\\Maths\\image_modif_2.png'))


print(get_element(85))
print()
print()
print("α^" + str(get_element(85).get_element_alpha_power()))
