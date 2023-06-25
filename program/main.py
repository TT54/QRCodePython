from QrCode import *


generate_qr_code("abcdefghij", 'D:\\Theo\\Cours\\Tipe\\Maths\\image.png')

print(read_qr_code('D:\\Theo\\Cours\\Tipe\\Maths\\image.png'))
print(read_qr_code('D:\\Theo\\Cours\\Tipe\\Maths\\image_modif.png'))
print(read_qr_code('D:\\Theo\\Cours\\Tipe\\Maths\\image_modif_2.png'))
