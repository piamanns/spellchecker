""" Function that calculates the Damerau-Levenshtein distance
    between two given words.

    Based on pseudocode in the Wikipedia article
    https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance,
    excellently explained by James M. Jensen II
    in https://www.lemoda.net/text-fuzzy/damerau-levenshtein/

    (Original blogpost available at
    https://web.archive.org/web/20180814145642/
    https://scarcitycomputing.blogspot.com/2013/04/damerau-levenshtein-edit-distance.html)
"""

from services.alphabet_utils import(
    CHAR_COUNT,
    calc_index
)


def calculate_dl_distance(word_a: str, word_b:str, debug_flag=False):
    """Calculates the Damerau-Levensthein distance between two words.

    Args:
        word_a: The source word as a string.
        word_b: The target word as a string.
        debug_flag: A boolean describing whether the matrix
                    resulting from the calculation should be
                    returned in its entirety (instead of
                    only the last cell containing the
                    final Damerau-Levenshtein distance).
                    Defaults to False.
    Returns:
        An integer describing the edit distance between the two words.
        Minimum value is 0, maximum the length of the longer word.
    """

    rows_per_char = [1] * CHAR_COUNT
    maxdist = len(word_a) + len(word_b)

    matrix = init_matrix(len(word_a) + 2, len(word_b) + 2, maxdist)

    for row in range(2, len(word_a) + 2):
        char_a = word_a[row-2]
        col_per_char = 0

        for col in range(2, len(word_b) + 2):
            char_b = word_b[col-2]
            #print(f"\nrow:{row}, col:{col}")
            row_w_match = rows_per_char[calc_index(char_b)]
            col_w_match = col_per_char

            if word_a[row-2] == word_b[col-2]:
                cost = 0
                col_per_char = col
            else:
                cost = 1

            matrix[row][col] = min(
                matrix[row-1][col-1] + cost, # substitution
                matrix[row][col-1] + 1, # insertion
                matrix[row-1][col] + 1, # deletion
                # transposition
                matrix[row_w_match-1][col_w_match-1]
                      + (row-row_w_match-1) + 1
                      + (col-col_w_match-1)
            )
            #minimum = calculate_min(matrix, row, col, cost, row_w_match, col_w_match)
            #matrix[row][col] = minimum

        rows_per_char[calc_index(char_a)] = row

    if debug_flag:
        return matrix
    return matrix[-1][-1]

def calculate_min(matrix, row, col, cost, row_w_match, col_w_match):
    """ Helper function for debugging purposes.

    Prints out the calculated values for substitution, insertion,
    deletion and transposition.

    Args:
        matrix: The matrix used for calculating the DL-distance.
        row: An integer representing the current row in the matrix.
        col: An integer representing the current column in the matrix.
        cost: The cost of a substitution edit (0 or 1).
        row_w_match: The latest row where the character in the current column
                     was seen.
        col_w_match: The latest column where the character in the current
                     row was seen.

    Returns:
        An integer representing the smallest edit distance value.
    """

    print("row_w_match", row_w_match, "col_w_match", col_w_match)

    subst = matrix[row-1][col-1] + cost
    insert = matrix[row][col-1] + 1
    delete = matrix[row-1][col] + 1
    transp = (matrix[row_w_match-1][col_w_match-1]
                + (row-row_w_match-1) + 1
                + (col-col_w_match-1)
    )
    print(f"subst:{subst}, insert:{insert}, delete:{delete}, transp:{transp}")
    return min(subst, insert, delete, transp)

def init_matrix(rows: int, cols: int, maxdist: int):
    """ Helper function for initializing the matrix.

    Args:
        rows: Number of rows in the matrix as an integer.
        cols: Number of columns in the matrix as an integer.
        maxdist: An integer representing a value large enough never
                to be chosen as smallest edit distance.

    Returns:
        The initialized matrix to be used in the calculating the
        Damerau-Levensthein distance.
    """

    mtx = [[0 for i in range(cols)] for j in range(rows)]
    mtx[0][0] = maxdist
    for i in range(1, rows):
        mtx[i][0] = maxdist
        mtx[i][1] = i - 1
    for j in range(1, cols):
        mtx[0][j] = maxdist
        mtx[1][j] = j - 1
    return mtx
