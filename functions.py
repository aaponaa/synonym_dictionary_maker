import stringdist
import numpy as np
import csv
from itertools import compress


def unique_list(col, data):
    list_of_col = data[str(col)].to_numpy()
    i = 0
    for x in list_of_col:
        list_of_col[i] = str(x)
        i += 1
    list_of_col = np.unique(list_of_col)
    list_of_col = np.sort(list_of_col)
    list_of_col = list_of_col.tolist()
    return list_of_col


def dico_sdist(fu_col, fu_tol, fu_word):
    it = 1
    for x in fu_col:
        temp_val = stringdist.levenshtein(str(x), fu_word)
        bool_list = [temp_val < fu_tol]

        if it == 1:
            r = bool_list
        else:
            r = r + bool_list
        it = it + 1

    filtered_list = list(compress(fu_col, r))
    return filtered_list


def to_my_csv(dico):
    with open('save.csv', 'w') as f:
        for key in dico.keys():
            f.write("%s, %s\n" % (key, dico[key]))
