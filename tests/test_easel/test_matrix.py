import pickle
import unittest

from pyhmmer.easel import Matrix, MatrixF, MatrixU8, Vector, VectorF, VectorU8


class _TestMatrixBase(object):

    Matrix = NotImplemented

    def test_pickle(self):
        v1 = self.Matrix([[1, 2], [3, 4]])
        v2 = pickle.loads(pickle.dumps(v1))
        for i in range(v1.shape[0]):
            for j in range(v1.shape[1]):
                self.assertEqual(v1[i,j], v2[i,j])

    def test_init(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        self.assertEqual(mat[0, 0], 1)
        self.assertEqual(mat[0, 1], 2)
        self.assertEqual(mat[1, 0], 3)
        self.assertEqual(mat[1, 1], 4)

    def test_init_error(self):
        self.assertRaises(ValueError, self.Matrix, [])
        self.assertRaises(ValueError, self.Matrix, [ [], [] ])
        self.assertRaises(ValueError, self.Matrix, [ [1.0, 2.0], [1.0] ])
        self.assertRaises(ValueError, self.Matrix.zeros, 0, 0)
        self.assertRaises(TypeError, self.Matrix, 1)
        self.assertRaises(TypeError, self.Matrix.zeros, [])

    def test_len(self):
        mat = self.Matrix([[1, 2], [3, 4]])
        self.assertEqual(len(mat), 2)
        mat = self.Matrix.zeros(10, 10)
        self.assertEqual(len(mat), 10)

    def test_min(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        self.assertEqual(mat.min(), 1)

    def test_max(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        self.assertEqual(mat.max(), 4)

    def test_argmin(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        self.assertEqual(mat.argmin(), (0, 0))
        mat = self.Matrix([ [2, 1], [4, 3] ])
        self.assertEqual(mat.argmin(), (0, 1))

    def test_argmax(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        self.assertEqual(mat.argmax(), (1, 1))
        mat = self.Matrix([ [2, 1], [4, 3] ])
        self.assertEqual(mat.argmax(), (1, 0))

    def test_copy(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        mat2 = mat.copy()
        del mat
        self.assertIsInstance(mat2, self.Matrix)
        self.assertEqual(mat2[0, 0], 1)
        self.assertEqual(mat2[0, 1], 2)
        self.assertEqual(mat2[1, 0], 3)
        self.assertEqual(mat2[1, 1], 4)

    def test_add_matrix(self):
        m1 = self.Matrix([ [1, 2], [3, 4] ])
        m2 = self.Matrix([ [2, 2], [3, 3] ])
        m3 = m1 + m2
        self.assertEqual(m3[0, 0], 3)
        self.assertEqual(m3[0, 1], 4)
        self.assertEqual(m3[1, 0], 6)
        self.assertEqual(m3[1, 1], 7)

    def test_add_scalar(self):
        m1 = self.Matrix([ [2, 2], [3, 3] ])
        m2 = m1 + 2.0
        self.assertEqual(m2[0, 0], 4)
        self.assertEqual(m2[0, 1], 4)
        self.assertEqual(m2[1, 0], 5)
        self.assertEqual(m2[1, 1], 5)

    def test_iadd_scalar(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        mat += 3
        self.assertEqual(mat[0, 0], 4)
        self.assertEqual(mat[0, 1], 5)
        self.assertEqual(mat[1, 0], 6)
        self.assertEqual(mat[1, 1], 7)

    def test_iadd_matrix(self):
        mat = self.Matrix([ [4, 5], [6, 7] ])
        mat += self.Matrix([ [2, 2], [3, 3] ])
        self.assertEqual(mat[0, 0], 6)
        self.assertEqual(mat[0, 1], 7)
        self.assertEqual(mat[1, 0], 9)
        self.assertEqual(mat[1, 1], 10)

    def test_mul_scalar(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        m2 = mat * 3
        self.assertEqual(m2[0, 0], 3)
        self.assertEqual(m2[0, 1], 6)
        self.assertEqual(m2[1, 0], 9)
        self.assertEqual(m2[1, 1], 12)

    def test_mul_matrix(self):
        mat = self.Matrix([ [3, 6], [9, 12] ])
        m2 = mat * self.Matrix([ [2, 2], [3, 3] ])
        self.assertEqual(m2[0, 0], 6)
        self.assertEqual(m2[0, 1], 12)
        self.assertEqual(m2[1, 0], 27)
        self.assertEqual(m2[1, 1], 36)

    def test_imul_scalar(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        mat *= 3
        self.assertEqual(mat[0, 0], 3)
        self.assertEqual(mat[0, 1], 6)
        self.assertEqual(mat[1, 0], 9)
        self.assertEqual(mat[1, 1], 12)

    def test_imul_matrix(self):
        mat = self.Matrix([ [3, 6], [9, 12] ])
        mat *= self.Matrix([ [2, 2], [3, 3] ])
        self.assertEqual(mat[0, 0], 6)
        self.assertEqual(mat[0, 1], 12)
        self.assertEqual(mat[1, 0], 27)
        self.assertEqual(mat[1, 1], 36)

    def test_sum(self):
        mat = self.Matrix([ [1, 2], [3, 4] ])
        self.assertEqual(mat.sum(), 1 + 2 + 3 + 4)


class TestMatrix(unittest.TestCase):

    def test_abstract(self):
        self.assertRaises(TypeError, Matrix, [ [1, 2], [3, 4] ])
        self.assertRaises(TypeError, Matrix.zeros, 2, 2)


class TestMatrixF(_TestMatrixBase, unittest.TestCase):

    Matrix = MatrixF

    def test_memoryview_tolist(self):
        mat = MatrixF([ [1, 2], [3, 4] ])
        mem = memoryview(mat)
        self.assertEqual(mem.tolist(), [ [1.0, 2.0], [3.0, 4.0] ])

    def test_getitem_row(self):
        mat = MatrixF([ [1, 2], [3, 4] ])

        self.assertIsInstance(mat[0], VectorF)
        self.assertEqual(list(mat[0]), [1.0, 2.0])
        self.assertEqual(list(mat[-1]), [3.0, 4.0])

        with self.assertRaises(IndexError):
            row = mat[-10]

    def test_getitem_element(self):
        mat = MatrixF([ [1, 2], [3, 4] ])

        self.assertEqual(mat[0, 0], 1.0)
        self.assertEqual(mat[0, 1], 2.0)
        self.assertEqual(mat[1, 0], 3.0)
        self.assertEqual(mat[1, 1], 4.0)

        self.assertEqual(mat[0, -1], 2.0)
        self.assertEqual(mat[-1, 0], 3.0)
        self.assertEqual(mat[-1, -1], 4.0)

        with self.assertRaises(IndexError):
            x = mat[-10, 0]
        with self.assertRaises(IndexError):
            x = mat[0, -10]
        with self.assertRaises(IndexError):
            x = mat[0, 10]
        with self.assertRaises(IndexError):
            x = mat[10, 0]


class TestMatrixU8(_TestMatrixBase, unittest.TestCase):

    Matrix = MatrixU8

    def test_memoryview_tolist(self):
        mat = MatrixU8([ [1, 2], [3, 4] ])
        mem = memoryview(mat)
        self.assertEqual(mem.tolist(), [ [1, 2], [3, 4] ])

    def test_getitem_row(self):
        mat = MatrixU8([ [1, 2], [3, 4] ])

        self.assertIsInstance(mat[0], VectorU8)
        self.assertEqual(list(mat[0]), [1, 2])
        self.assertEqual(list(mat[-1]), [3, 4])

        with self.assertRaises(IndexError):
            row = mat[-10]

    def test_getitem_element(self):
        mat = MatrixU8([ [1, 2], [3, 4] ])

        self.assertEqual(mat[0, 0], 1)
        self.assertEqual(mat[0, 1], 2)
        self.assertEqual(mat[1, 0], 3)
        self.assertEqual(mat[1, 1], 4)

        self.assertEqual(mat[0, -1], 2)
        self.assertEqual(mat[-1, 0], 3)
        self.assertEqual(mat[-1, -1], 4)

        with self.assertRaises(IndexError):
            x = mat[-10, 0]
        with self.assertRaises(IndexError):
            x = mat[0, -10]
        with self.assertRaises(IndexError):
            x = mat[0, 10]
        with self.assertRaises(IndexError):
            x = mat[10, 0]
