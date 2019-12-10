from unittest import mock
from tool.mock_test.add_api import Count
import unittest


class TestCount(unittest.TestCase):

	def test_add(self):
		count = Count()
		count.add = mock.Mock(return_value=10, side_effect=count.add)
		result = count.add(1, 19)
		count.add.assert_called_with(8, 8)
		self.assertEqual(result, 10)


if __name__ == '__main__':
	unittest.main()
