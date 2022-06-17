from itertools import compress

import numpy as np
import pandas as pd
import stringdist


class SynonymDataSource:

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data = pd.read_csv(file_name, encoding="UTF-8")
        self.columns = self.data.columns.values

    def search_synonyms(self, column: str, word: str, tolerance: float):
        return self._dico_sdist(self._unique_list(column), word, tolerance)

    def _unique_list(self, column: str):
        list_of_col = self.data[str(column)].to_numpy()
        for (i, x) in enumerate(list_of_col):
            list_of_col[i] = str(x)
        list_of_col = np.unique(list_of_col)
        list_of_col = np.sort(list_of_col)
        list_of_col = list_of_col.tolist()
        return list_of_col

    def _dico_sdist(self, values, word: str, tolerance: float):
        for (i, x) in enumerate(values):
            temp_val = stringdist.levenshtein(str(x), word)
            bool_list = [temp_val < tolerance]
            r = bool_list if i == 0 else r + bool_list

        filtered_list = list(compress(values, r))
        return list(set([s.strip() for s in filtered_list]))

    def export(self, file_name: str, data: dict):
        if ".csv" not in file_name:
            file_name += ".csv"
        with open(file_name, 'w') as f:
            f.write("%s, %s, %s, %s\n" % ("column", "word", "tolerance", "synonyms"))
            for t in data:
                f.write("%s, %s, %s, %s\n" % (t[0], t[1], t[2], t[3]))
