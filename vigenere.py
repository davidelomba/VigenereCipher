import math
import re
from collections import Counter
from functools import reduce

import numpy as np

# vettore delle frequenze percentuali delle lettere nella lingua inglese
p = [8.17, 0.15, 2.78, 4.03, 12.7, 0.15, 6.33, 6.09, 6.97, 0.1, 0.05, 4.25, 2.41,
     6.75, 7.51, 1.49, 1.93, 9.06, 6.75, 6.09, 5.99, 0.98, 2.23, 2.02, 1.97, 0.77]
def letter_to_number(plain):
    # converto tutte le lettere in minuscolo
    plain = plain.lower()
    number = []

    for c in plain:
        if 'a' <= c <= 'z':
            # aggiungo ogni numero alla lista "number"
            number.append(ord(c) - ord('a'))
    return number

def number_to_letter(number):
    return chr(int(number) + ord('a'))

def matrix_to_string(matrix):
    result_string = ""

    for col in range(matrix.shape[1]):
        for row in range(matrix.shape[0]):
            result_string += number_to_letter(matrix[row, col])

    print("Stringa risultante: ", result_string)
    print()
def input_ciphertext():
    input_str = input("Inserisci il ciphertext (digita 'fine' per terminare): ")

    # creo la stringa considerando ogni riga. Appena all'inizio di una riga viene scritto fine, termina l'esecuzione del while
    while True:
        row = input()
        if row.lower() == "fine":
            break
        input_str += row + "\n"

    input_str = re.sub(r'[^a-zA-Z]', '', input_str).lower()
    return input_str


def Ic(m_grams_count):
    # calcolo la somma di tutti gli m-grams
    total_grams = sum(m_grams_count.values())
    ic_value = 0
    # calcolo l'indice di coincidenza moltiplicando, per ogni m-gram, la sua frequenza per "frequenza - 1".
    # Infine divido per il numero totale degli m-grams moltiplicato per "numero totale degli m-grams - 1"
    for item in m_grams_count.values():
        ic_value += (item*(item - 1))
    ic_value = ic_value/(total_grams*(total_grams - 1))
    return ic_value

def count_m_grams(s, m):
    m_grams = [s[i:i + m] for i in range(0, len(s) - m + 1, m)]
    # crea un dizionario in cui le chiavi sono gli m-grams e i valori le relative frequenze
    m_grams_count = Counter(m_grams)

    print(m_grams_count)
    print()
    return m_grams_count

# funzione che restituisce la chiave (quindi il gram) che ha il maggior numero di occorrenze
def max_gram(m_grams_count):
    max_gram = max(m_grams_count, key=m_grams_count.get)

    print("Gram con più occorrenze: ", max_gram)
    print()
    return max_gram

# funzione per il calcolo delle distanze tra la prima occorrenza di un gram e le altre
def distance_gram(s, gram):
    pos = []

    # Trova tutte le posizioni in cui l'm-gram appare nella stringa
    for i in range(0, len(s) - len(gram) + 1, len(gram)):
        check_gram = s[i:i + len(gram)]

        if check_gram == gram:
            # aggiungo 1 perché la posizione della prima lettera del ciphertext è 1 e non 0
            pos.append(i + 1)

    print("Posizioni:", pos)
    print()

    dist = []
    if pos:
        first_gram = pos[0]

        for i in range(1, len(pos)):
            dist_gram = pos[i] - first_gram
            dist.append(dist_gram)

    print("Distanze:", dist)
    print()
    return dist

# funzione che calcola il MCD delle distanze
def mcd_dist(dist):
    return reduce(math.gcd, dist)

# funzione che costruisce la matrice (m,n') con n' = n/m se m divide n altriment n' = int(n/m) + 1
def build_matrix(s, m):
    if (len(s) % m) == 0:
        n = len(s)/m
    else:
        n = int(len(s) / m) + 1

    matrix = np.zeros((m, n))
    i = 0

    for col in range(n):
        for row in range(m):
            if i < len(s):
                matrix[row, col] = s[i]
                i += 1

    # print(matrix)
    return matrix

# funzione che calcola l'indice di coincidenza per ogni riga della matrice
def matrix_ic(matrix):
    ic = []

    for i in range(matrix.shape[0]):
        row = matrix[i, :]
        gram_count = Counter(row)
        ic_gram = Ic(gram_count)
        ic.append(ic_gram)

    print("Indice di coincidenza: ", ic)
    print()
    return ic

# funzione che calcola le frequenze relative dei caratteri di ciascuna riga della matrice
def freq_calc(row):
    freq_counter = Counter(row)
    total_count = len(row)

    freq = {}

    for k, v in freq_counter.items():
        freq[k] = v / total_count

    return freq

# funzione che calcola M per un dato g
def M_calc(freq, g):
    result = 0
    for j in range(26):
        index = (g + j) % 26
        freq_value = freq.get(index, 0)

        result += (p[j] * freq_value)/100

    return result

# funzione per il calcolo della chiave
def key_calc(matrix):
    # rappresenta il massimo M per ogni riga
    max_m = []
    # rappresenta la chiave
    max_g = []

    # il ciclo esterno itera per ogni riga della matrice
    for i in range(matrix.shape[0]):
        # matrice che contiene i valori di M per ogni g da 0 a 25 (fissata una riga)
        mat_g = np.zeros((26, 1))
        row = matrix[i, :]
        freq = freq_calc(row)
        # per ogni g calcolo M
        for g in range(26):
            result = M_calc(freq, g)
            mat_g[g, 0] = result
        # prendo il massimo degli M al variare di g
        max_m_row = np.max(mat_g)
        # salvo g corrispndente al massimo M
        max_m_row_index = np.argmax(mat_g)
        max_m.append(max_m_row)
        max_g.append(max_m_row_index)
    return max_g, max_m

# funzione per la decifratura del messaggio
def decrypt(matrix, key):
    matrix = np.array(matrix)
    key = np.array(key)
    result = (matrix - key[:, np.newaxis]) % 26
    # print(result)
    # print()
    return result


if __name__ == '__main__':
    input_str = input_ciphertext()
    # il secondo parametro di count_m_grams indica la grandezza di ogni gram
    m_grams_count = count_m_grams(input_str, 4)
    # trovo il gram che ha il più alto numero di occorrenze
    gram = max_gram(m_grams_count)
    # calcolo le distanze tra le occorrenze
    dist = distance_gram(input_str, gram)
    # calcolo il MCD tra le distanze
    m = mcd_dist(dist)
    print("Lunghezza chiave ipotizzata (MCD): ", m)
    print()
    # converto in numeri il ciphertext
    s = letter_to_number(input_str)
    # print(s)
    # costruisco la matrice in base alla lunghezza della chiave ipotizzata
    matrix = build_matrix(s, m)
    # calcolo l'indice di coincidenza di ogni riga per verificare la correttezza della lunghezza della chiave
    ic = matrix_ic(matrix)
    # calcolo la chiave
    max_g, max_m = key_calc(matrix)

    print("Chiave: ", max_g)

    print()

    print(max_m)

    print()

    # decifro il ciphertext
    result = decrypt(matrix, max_g)

    # stampo il messaggio cifrato dopo aver convertito i numeri in lettere
    matrix_to_string(result)