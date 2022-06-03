import unittest

from services.distance_service import(
    calculate_dl_distance,
    init_matrix
)

class TestDistanceService(unittest.TestCase):

    def test_substituted_char_returns_correct_distance(self):
        dl_distance = calculate_dl_distance("definately", "definitely")
        self.assertEqual(dl_distance, 1)

    def test_inserted_chars_returns_correct_result(self):
        dl_distance = calculate_dl_distance("glamourouse", "glamorous")
        self.assertEqual(dl_distance, 2)
    
    def test_deleted_chars_returns_correct_result(self):
        dl_distance = calculate_dl_distance("interupt", "interrupt")
        self.assertEqual(dl_distance, 1)

        dl_distance = calculate_dl_distance("car", "carbon")
        self.assertEqual(dl_distance, 3)
    
    def test_transposition_of_chars_returns_correct_result(self):
        dl_distance = calculate_dl_distance("teh", "the")
        self.assertEqual(dl_distance, 1)
    
    def test_several_typing_errors_returns_correct_result(self):
        dl_distance = calculate_dl_distance("vbarrtndre", "bartender")
        self.assertEqual(dl_distance, 4)

    def test_matrix_is_initialized_correctly(self):
        matrix = init_matrix(5, 6, 7)
 
        self.assertEqual(len(matrix), 5)
        self.assertEqual(len(matrix[0]), 6)

        row_0 = matrix[0]
        row_1 = matrix[1]
        row_2 = matrix[2]

        col_0 = []
        col_1 = []
        col_2 = []

        for i in range(len(matrix)):
            col_0.append(matrix[i][0])
            col_1.append(matrix[i][1])
            col_2.append(matrix[i][2])

        self.assertListEqual(row_0, [7, 7, 7, 7, 7, 7])
        self.assertListEqual(row_1, [7, 0, 1, 2, 3, 4])
        self.assertListEqual(row_2, [7, 1, 0, 0, 0, 0])

        self.assertListEqual(col_0, [7, 7, 7, 7, 7])
        self.assertListEqual(col_1, [7, 0, 1, 2, 3])
        self.assertListEqual(col_2, [7, 1, 0, 0, 0])

    def test_matrix_is_returned_when_debug_flag_set_to_True(self):
        word_source = "craton"
        word_target = "cartoon"
        dl_distance = calculate_dl_distance(word_source, word_target)
        matrix = calculate_dl_distance(word_source, word_target, True)
        self.assertEqual(len(matrix), len(word_source) + 2)
        self.assertEqual(len(matrix[0]), len(word_target) + 2)
        self.assertEqual(matrix[-1][-1], dl_distance)

    def test_matrix_content_is_calculated_correctly(self):
        word_source = "zbar"
        word_target = "zebra"
        matrix = calculate_dl_distance(word_source, word_target, True)
        rows = []
        cols = len(word_target) + 2
        max_cost = len(word_source) + len(word_target)
        rows.append([max_cost for i in range(cols)])
        rows.append([max_cost] + list(range(len(word_target)+1)))
        rows.append([max_cost, 1, 0, 1, 2, 3, 4])
        rows.append([max_cost, 2, 1, 1, 1, 2, 3])
        rows.append([max_cost, 3, 2, 2, 2, 2, 2])
        rows.append([max_cost, 4, 3, 3, 3, 2, 2])

        for i, row in enumerate(rows):
            self.assertListEqual(matrix[i], row)
