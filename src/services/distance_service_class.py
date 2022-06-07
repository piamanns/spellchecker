from services.alphabet_utils import(
    CHAR_COUNT,
    calc_char,
    calc_index
)

class DistanceServiceRecursive:
    def __init__(self):
        self._trie = None
        self._matrix = None
        self._word_target = None
        self._max_edit = None
        self._candidates = None
        self._big_cost = None

    def calculate_dl_distance(self, word_target: str, trie, max_edit=None):
        self._trie = trie
        self._word_target = word_target
        self._max_edit = max_edit
        self._candidates = {}
        self._big_cost = trie.get_max_keylength()

        first_char_nodes = trie.get_root().children

        for i, node in enumerate(first_char_nodes):
            if node:
                rows_per_char = [1] * CHAR_COUNT
                self._matrix = [[self._big_cost for j in range (len(word_target) + 2)]]
                self._matrix += [[self._big_cost] + list(range(len(word_target) + 1))]
                letter = calc_char(i)

                self._calculate(node, letter, "", 1, rows_per_char)

        if self._candidates.keys():
            return self._candidates[min(self._candidates.keys())]
        return []

    def _calculate(self, node, char_source, word_source,
                   prev_row_idx, rows_per_char):

        cols = len(self._word_target) + 2
        col_per_char = 0
        curr_row = [self._big_cost, self._matrix[prev_row_idx][1] + 1]

        for col in range(2, cols):
            char_target = self._word_target[col-2]
            #print("comparing ", char_source, " to ", char_target)
            #print("source word is now", word_source+char_source)

            row_w_match = rows_per_char[calc_index(char_target)]
            col_w_match = col_per_char

            if char_source == char_target:
                cost = 0
                col_per_char = col
            else:
                cost = 1

            smallest_cost = self._calculate_min(curr_row, prev_row_idx,
                                                col, cost, row_w_match,
                                                col_w_match)
            curr_row.append(smallest_cost)

        self._matrix.append(curr_row)

        tmp = rows_per_char[calc_index(char_source)]
        rows_per_char[calc_index(char_source)] = prev_row_idx + 1

        max_cost = self._max_edit if self._max_edit else self._big_cost

        if node.is_valid_end and curr_row[-1] <= max_cost:
            self._add_word_as_candidate(word_source+char_source, curr_row[-1])
            self._max_edit = curr_row[-1]

        for i, child in enumerate(node.children):
            if child and min(curr_row) <= max_cost:
                self._calculate(child, calc_char(i), word_source+char_source,
                    prev_row_idx+1, rows_per_char
                )

        rows_per_char[calc_index(char_source)] = tmp
        self._matrix.pop()

    def _calculate_min(self, curr_row, prev_row_idx, col, cost, row_w_match, col_w_match):
        subst = self._matrix[prev_row_idx][col-1] + cost
        insert = curr_row[col-1] + 1
        delete = self._matrix[prev_row_idx][col] + 1
        transp = (self._matrix[row_w_match-1][col_w_match-1]
                  + (prev_row_idx-row_w_match) + 1
                  + (col-col_w_match-1)
        )
        #print(f"subst:{subst}, insert:{insert}, delete:{delete}, transp:{transp}")
        return min(subst, insert, delete, transp)

    def _add_word_as_candidate(self, word, dl_distance):
        if dl_distance not in self._candidates:
            self._candidates[dl_distance] = []
        self._candidates[dl_distance].append(f"{word}({dl_distance})")
