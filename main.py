import math
import os
import PySimpleGUI as sg
import numpy as np

alphabet = "aábcčdeéfghijklmnoprsštuvzž"
alphabet_upper = "aábcčdeéfghijklmnoprsštuvzž".upper()
other_characters = "\n\"\';:?!.,- "

alphabet = alphabet + alphabet_upper + other_characters

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod_inv(matrix, mod):
    d = np.linalg.det(matrix)
    determinant = int(np.round(d))
    determinant_inverse = pow(determinant, -1, mod) % mod
    matrix_modulus_inv = (
            determinant_inverse * np.round(determinant * np.linalg.inv(matrix)).astype(int) % mod
    )
    return matrix_modulus_inv


def encrypt(text, K):
    encrypted = ""
    text_in_numbers = [letter_to_index[letter] for letter in text]

    split_P = [
        text_in_numbers[i: i + int(K.shape[0])]
        for i in range(0, len(text_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index["a"])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted


def decrypt(cipher, key_inv):
    decrypted = ""
    cipher_in_numbers = [letter_to_index[letter] for letter in cipher]

    split_C = [
        cipher_in_numbers[i: i + int(key_inv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(key_inv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(key_inv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


def start_gui():
    layout = [
        [sg.Text('Datoteka'), sg.InputText(), sg.FileBrowse('Išči')],
        [sg.Text('Ključ'), sg.InputText()],
        [sg.Output(size=(88, 20))],
        [sg.Submit(button_text='Šifriraj'), sg.Cancel(button_text='Zapri')]
    ]
    window = sg.Window('Hillova šifra', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel', 'Zapri'):
            break
        if event == 'Submit' or event == 'Šifriraj':
            filepath = key = is_validation_ok = None
            if values[0] and values[1]:
                filepath = values[0]
                key = values[1]
                is_validation_ok = True
                if not filepath and filepath is not None:
                    print('Napaka: pot do datoteke ni pravilna.')
                    is_validation_ok = False
                elif not key and key is not None:
                    print('Napaka: Ključ ni v pravilni obliki.')
                    is_validation_ok = False
                elif is_validation_ok:
                    try:
                        # izračun dimenzije matrike ključa
                        r_shape = int(math.sqrt(len(key)))
                        mtx = np.array([int(letter_to_index[letter]) for letter in key]).reshape(r_shape, r_shape)

                        key_in_num = np.matrix(mtx)
                        key_in_num_inv = matrix_mod_inv(key_in_num, len(alphabet))

                        with open(filepath, 'rt', encoding="utf-8") as data:
                            raw_data = data.read()
                            encrypted_file = encrypt(raw_data, key_in_num)
                            decrypted_file = decrypt(encrypted_file, key_in_num_inv)

                            print('Pot datoteke:', filepath)
                            print('Ključ: ', key, mtx)
                            print("DATA: ", len(raw_data))
                            print("Originalna velikost datoteke: ", os.path.getsize(filepath))
                            print("------------------------------------------------")
                            print("Šifrirana datoteka: ", encrypted_file)
                            print("------------------------------------------------")
                            print("Dešifrirana datoteka: ", decrypted_file)
                            # print("Velikost datotek: ", len(raw_data), len(decrypted_file))
                    except:
                        print('*** Napaka: izbrani ključ ni primeren ***')
            else:
                print('Napaka pri vnosnih poljih')
    window.close()


if __name__ == '__main__':
    start_gui()
