
class NominalTransformation:

    def __init__(self):
        pass

    @staticmethod
    def levenshtain_distance(str1, str2):
        j = []
        for ind_j in range(0, len(str2)):
            i = []
            j.append(i)
            for ind_i in range(0, len(str1)):
                if ind_j == 0 or ind_i == 0:
                    if ind_j != ind_i:
                        diagonal = abs(ind_j - ind_i) - 1
                    else:
                        diagonal = 0
                else:
                    diagonal = j[ind_j - 1][ind_i - 1]

                i.append(min(ind_j + 1 if ind_i == 0 else i[ind_i - 1] + 1,
                             ind_i + 1 if ind_j == 0 else j[ind_j - 1][ind_i] + 1,
                             diagonal + int(str2[ind_j] != str1[ind_i]))
                         )

        for ind in range(0, len(j)):
            print j[ind]
