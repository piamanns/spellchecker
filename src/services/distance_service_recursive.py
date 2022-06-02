from services.alphabet_utils import(
    CHAR_COUNT,
    calc_index,
    calc_char
)

def calculate_dl_distance_recursive(word_target: str, trie, max_edit: int):
    first_char_nodes = trie.get_root().children
    candidates = {}
    big_cost = trie.get_max_keylength()

    for i, node in enumerate(first_char_nodes):
        if node:
            rows_per_char = [1] * CHAR_COUNT
            matrix = [[big_cost for j in range (len(word_target) + 2)]]
            matrix += [[big_cost] + list(range(len(word_target) + 1))]
            letter = calc_char(i)

            calculate(
                node, letter, "", word_target,
                1, matrix, rows_per_char, max_edit,
                big_cost, candidates
            )

    for i in range(big_cost):
        if i in candidates:
            return candidates[i]
    return []

def calculate(node, char_source, word_source, word_target,
              prev_row_idx, matrix, rows_per_char, max_edit,
              big_cost, candidates):

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

    if node.is_valid_end:
        dl_distance = curr_row[-1]
        if dl_distance not in candidates:
            candidates[dl_distance] = []
        candidates[dl_distance].append(f"{word_source+char_source}({curr_row[-1]})")

    for i, child in enumerate(node.children):
        if child and not (max_edit and min(curr_row) > max_edit):
            calculate(child, calc_char(i), word_source+char_source, word_target,
                prev_row_idx+1, matrix, rows_per_char,
                max_edit, big_cost, candidates
            )

    rows_per_char[calc_index(char_source)] = tmp
    matrix.pop()


def calculate_min(matrix, curr_row, prev_row_idx, col, cost, row_w_match, col_w_match):
    subst = matrix[prev_row_idx][col-1] + cost
    insert = curr_row[col-1] + 1
    delete = matrix[prev_row_idx][col] + 1
    transp = (matrix[row_w_match-1][col_w_match-1]
                + (prev_row_idx-row_w_match) + 1
                + (col-col_w_match-1)
    )
    #print(f"subst:{subst}, insert:{insert}, delete:{delete}, transp:{transp}")
    return min(subst, insert, delete, transp)
