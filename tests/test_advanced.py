import unittest
import context

import audiobook.core


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(audiobook.core.hmm())


if __name__ == "__main__":
    unittest.main()
