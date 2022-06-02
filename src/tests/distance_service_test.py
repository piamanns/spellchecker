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
 