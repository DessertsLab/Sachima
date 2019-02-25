import unittest
from sachima import tools


class TestA(unittest.TestCase):
    def test_tools(self):
        assert tools.lengthOfLongestSubstring("abcabcbb") == 3

    def another_test():
        pass


if __name__ == "__main__":
    unittest.main()
