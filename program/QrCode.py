from PIL import Image
import numpy as np
from ReedSolomon import *


def show_image(m, file_name, zoom=1):
    x = 255 * np.asarray(m, dtype=np.uint8)
    im = Image.fromarray(x)
    if zoom > 1:
        im = im.resize((im.size[0]*zoom, im.size[1]*zoom), Image.NEAREST)
    elif max(im.size) < 100:
        im = im.resize((im.size[0]*10, im.size[1]*10), Image.NEAREST)
    im.show()
    im.save(file_name)


def taille(m):
    """ Renvoie le tuple longueur, largeur de l'image m"""
    return len(m[0]), len(m)


def image_nb_vide(w,h):
    """ Renvoie une image vide NB (noire) de taille w x h"""
    m = []
    for j in range(h):
        l = []
        for i in range(w):
            l.append(1)
        m.append(l)
    return m


black = 0
white = 1


def string_to_bytes_list(input):
    """Renvoie une liste d'entiers représentant la chaine de caractère encodée"""
    str_bytes = bytes(input, "iso-8859-1")
    encoded = []
    for byte in str_bytes:
        encoded.append(byte)
    return encoded


def get_code_with_infos(to_encode):
    """Rajoute à la liste d'entiers à encoder sa taille en premier élément"""
    result = [len(to_encode)]
    for i in to_encode:
        result.append(i)
    return result


def bytes_to_binary_array(data):
    """Renvoie à partir de la liste d'octets une liste de bits (booleans) qui les représentent"""
    bits = []
    for i in data:
        bits += get_binary_from_byte(i)
    return bits


def get_binary_from_byte(byte):
    """Renvoie une liste de bits (booleans) associés à un octet"""
    converted = [False] * 8
    range = 7
    while byte >= 1:
        r = byte % 2
        converted[range] = r == 1
        range -= 1
        byte = byte // 2
    return converted

def binary_to_bytes_array(data):
    """Renvoie une liste d'octets à partir d'une liste de bits"""
    bytes_data = [0] * (len(data) // 8)
    for i in range(len(data) // 8):
        for j in range(8):
            bytes_data[i] += 2 ** (7 - j) if data[i * 8 + j] else 0
    return bytes_data


def add_error_correction(encoded_data):
    """Encode les données avec l'algorithme de Reed Solomon"""
    return encode(encoded_data)


def write_base_matrix(matrix):
    """Ajoute par effet de bord à une matrice la basse du QR-Code"""
    l = len(matrix)

    for i in range(7):
        matrix[0][i] = black
        matrix[l - 7][i] = black
        matrix[0][l - 1 - i] = black

        matrix[6][i] = black
        matrix[l - 1][i] = black
        matrix[6][l - 1 - i] = black

    for i in range(5):
        matrix[1 + i][0] = black
        matrix[l - 1 - 1 - i][0] = black
        matrix[1 + i][l - 1] = black

        matrix[1 + i][6] = black
        matrix[l - 1 - 1 - i][6] = black
        matrix[1 + i][l - 7] = black

    for i in range(3):
        for j in range(3):
            matrix[2 + i][2 + j] = black
            matrix[l - 1 - 2 - i][2 + j] = black
            matrix[2 + i][l - 1 - 2 - j] = black

        matrix[l - 1 - 8 - 2 * i][4] = black
        matrix[4][8 + 2 * i] = black


def encode_data_into_matrix(matrix, datas):
    """Ajoute à la matrice les données (chaine de bits) par effet de bord"""
    l = len(matrix)

    for i in range(len(datas) // 8):
        for j in range(8):
            data = datas[i * 8 + j]

            if(i < 12):
                row = (i % 3) * 4 + (j // 2)
                column = (i // 3) * 2 + (j % 2)

                matrix[l - 1 - row][l - 1 - column] = white if data else black
            elif(i < 22):
                row = ((i - 12) % 5) * 4 + (j // 2)
                if((i - 12) % 5 == 4):
                    row += 1

                column = ((i - 12) // 5) * 2 + (j % 2) + 8

                matrix[l - 1 - row][l - 1 - column] = white if data else black
            elif(i < 24):
                row = 8 + j // 2
                column = 12 + (i - 22) * 2 + (j % 2)

                matrix[l - 1 - row][l - 1 - column] = white if data else black
            elif(i < 26):
                row = 8 + j // 2
                column = 17 + (i - 24) * 2 + (j%2)

                matrix[l - 1 - row][l - 1 - column] = white if data else black


def generate_qr_code(text, file_name="D:\\Theo\\Cours\\Tipe\\Maths\\image.png"):
    """Affiche l'image générée à partir d'un message"""
    matrix = image_nb_vide(21, 21)
    write_base_matrix(matrix)
    data = string_to_bytes_list(text)

    encode_data_into_matrix(matrix, bytes_to_binary_array(encode_bytes(data)))
    show_image(matrix, file_name)


def read_qr_code(image_path):
    matrix = np.array(Image.open(image_path).convert('1').resize((21,21)),dtype='uint8').tolist()
    l = len(matrix)
    datas = [0] * 26 * 8

    for i in range(26):
        for j in range(8):
            if i < 12:
                row = (i % 3) * 4 + (j // 2)
                column = (i // 3) * 2 + (j % 2)

                datas[i * 8 + j] = matrix[l - 1 - row][l - 1 - column] == white
            elif i < 22:
                row = ((i - 12) % 5) * 4 + (j // 2)
                if (i - 12) % 5 == 4:
                    row += 1

                column = ((i - 12) // 5) * 2 + (j % 2) + 8

                datas[i * 8 + j] = matrix[l - 1 - row][l - 1 - column] == white
            elif i < 24:
                row = 8 + j // 2
                column = 12 + (i - 22) * 2 + (j % 2)

                datas[i * 8 + j] = matrix[l - 1 - row][l - 1 - column] == white
            elif i < 26:
                row = 8 + j // 2
                column = 17 + (i - 24) * 2 + (j % 2)

                datas[i * 8 + j] = matrix[l - 1 - row][l - 1 - column] == white

    decoded = decode_bytes(binary_to_bytes_array(datas))

    return bytes(decoded[2 * t:]).decode('iso-8859-1')
