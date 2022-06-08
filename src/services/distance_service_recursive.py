""" Function that recursively calculates the Damerau-Levenshtein distance
    between a given word and all keys in a trie data structure.

    Implementation idea:
    There is no need to recalculate the whole matrix needed for
    the Damerau-Levenshtein algorithm for words that share the same prefix
    in the trie: just adding a new row for the next letter will suffice.
    This recursive approach speeds up the search for possible correctly
    spelled candidate words significantly.

    Based on Steve Hanov's very informative blog post on
    http://stevehanov.ca/blog/index.php?id=114.

    The following implementation also takes the possibility of the transposition
    of two characters into account.
"""


from services.alphabet_utils import(
    CHAR_COUNT,
    calc_index,
    calc_char
)


def calculate_dl_distance_recursive(word_target: str, trie, max_dist=None):
    """ Calculates the Damerau-Lewenshtein distance between the given word
        and all words in the given trie.

    Args:
        word_target: A string representing the word to be matched
                     with the words in the trie (used as the target word).
        trie: A Trie-object containing the words in the wordlist.
        max_dist: The maximum Damerau-Lewenshtein distance allowed.
                  Defaults to None.

    Returns:
        A list containing the word(s) from the trie with the lowest
        Damerau-Levenshtein distance to the given word.
    """

    first_char_nodes = trie.get_root().children
    candidates = {}
    big_cost = trie.get_max_keylength()

    curr_max_dist = max_dist if max_dist else big_cost

    for i, node in enumerate(first_char_nodes):
        if node:
            rows_per_char = [1] * CHAR_COUNT
            matrix = [[big_cost for j in range (len(word_target) + 2)]]
            matrix += [[big_cost] + list(range(len(word_target) + 1))]
            letter = calc_char(i)

            #print("current max dist is: ", curr_max_dist)
            curr_max_dist = calculate(
                                node, letter, "", word_target,
                                1, matrix, rows_per_char, curr_max_dist,
                                big_cost, candidates
                            )

    if candidates.keys():
        return candidates[min(candidates.keys())]
    return []

def calculate(node, char_source, word_source, word_target,
              prev_row_idx, matrix, rows_per_char, max_dist,
              big_cost, candidates):
    """ A recursive function for filling in the next row
        in the matrix.

    Args:
        node: The current node in the trie as a Node-object.
        char_source: A string representing the letter in the word from the
                     trie being currently handled.
        word_source: A string holding the prefix handled so far.
        word_target: A string representing he word we are trying to find
                     a close match for in the trie.
        prev_row_idx: The index of the previous row in the matrix as
                      an integer.
        matrix: The matrix used for the Damerau-Levenshtein algorithm.
        rows_per_char: A list containing the indexes of rows where letters
                       were last seen. The list is indexed by the ordinal number
                       of the letters in the used alphabet.
        max_dist: The maximum Damerau-Levenshtein distance allowed as an integer.
        big_cost: An integer representing a DL-distance large enough never to
                  be chosen.
        candidates: A dict containing candidate words for the correct spelling of
                    the given word. Keys are the Damerau-Levenshtein distances,
                    values lists containing words from the trie with that particular
                    Damerau-Levenshtein distance to the given word.
    """

    cols = len(word_target) + 2
    col_per_char = 0
    curr_row = [big_cost, matrix[prev_row_idx][1] + 1]

    for col in range(2, cols):
        char_target = word_target[col-2]
        #print("comparing ", char_source, " to ", char_target)
        #print("source word is now", word_source+char_source)

        row_w_match = rows_per_char[calc_index(char_target)]
        col_w_match = col_per_char

        if char_source == char_target:
            cost = 0
            col_per_char = col
        else:
            cost = 1

        smallest_cost = calculate_min(matrix, curr_row, prev_row_idx,
                                      col, cost, row_w_match,
                                      col_w_match)
        curr_row.append(smallest_cost)

    matrix.append(curr_row)

    tmp = rows_per_char[calc_index(char_source)]
    rows_per_char[calc_index(char_source)] = prev_row_idx + 1

    curr_max_dist = max_dist if max_dist else big_cost

    if node.is_valid_end and curr_row[-1] <= curr_max_dist:
        add_word_as_candidate(candidates, word_source+char_source, curr_row[-1])
        curr_max_dist = curr_row[-1]

    for i, child in enumerate(node.children):
        if child and min(curr_row) <= curr_max_dist:
            curr_max_dist = calculate(child, calc_char(i), word_source+char_source, word_target,
                prev_row_idx+1, matrix, rows_per_char, curr_max_dist,
                big_cost, candidates
            )

    rows_per_char[calc_index(char_source)] = tmp
    matrix.pop()
    return curr_max_dist


def calculate_min(matrix, curr_row, prev_row_idx, col, cost, row_w_match, col_w_match):
    """ A helper function for calculating the smallest Damerau-Levenshtein-distance
        value for the current cell in the matrix.

    Args:
        matrix: The matrix used for calculating the Damerau-Levenshtein distance.
        curr_row: A list containing the edit costs in the current row so far.
        prev_row_idx: An integer representing the index number of the previous row.
        col: The index number of the current column as an integer.
        cost: The cost of a substitution edit (0 or 1).
        row_w_match: The latest row where the character in the current column
                     was seen.
        col_w_match: The latest column where the character in the current
                     row was seen.

    Returns:
        An integer representing the smallest edit distance value.
    """

    subst = matrix[prev_row_idx][col-1] + cost
    insert = curr_row[col-1] + 1
    delete = matrix[prev_row_idx][col] + 1
    transp = (matrix[row_w_match-1][col_w_match-1]
                + (prev_row_idx-row_w_match) + 1
                + (col-col_w_match-1)
    )
    #print(f"subst:{subst}, insert:{insert}, delete:{delete}, transp:{transp}")
    return min(subst, insert, delete, transp)

def add_word_as_candidate(candidates, word, dl_distance):
    """ Adds word as candidate for correct spelling

    Args:
        candidates: Dict holding candidate words. Keys are Damerau-Levenshtein distances,
                    values lists of candidate words with that particular distance.
        word: The candidate word to be added as a string.
        dl_distance: An integer describing the Damera-Levenshtein distance.
    """
    if dl_distance not in candidates:
        candidates[dl_distance] = []
    candidates[dl_distance].append(f"{word}({dl_distance})")
