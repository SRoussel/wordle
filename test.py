"""Unit tests."""

import unittest
import guess

class TestNext(unittest.TestCase):
    """Test wordle."""

    def test_valid_case(self):
        """Only lowercase words are valid."""
        self.assertTrue(guess.valid("valid"))
        self.assertFalse(guess.valid("VaLiD"))
        self.assertFalse(guess.valid("VALID"))

    def test_valid_length(self):
        """Only WORDLE_SIZE length words are valid."""
        self.assertFalse(guess.valid("arisen"))
        self.assertFalse(guess.valid("rise"))

    def test_valid_numbers(self):
        """Numbers are invalid."""
        self.assertFalse(guess.valid("val1d"))
        self.assertFalse(guess.valid("12345"))

    def test_evaluate(self):
        """Test evaluation. None corresponds to incorrect, False to wrong place,
            True to correct place."""
        self.assertEqual(guess.evaluate("abcde", "abcde"), [True, True, True, True, True])
        self.assertEqual(guess.evaluate("zbcde", "abcde"), [None, True, True, True, True])
        self.assertEqual(guess.evaluate("edcba", "abcde"), [False, False, True, False, False])
        self.assertEqual(guess.evaluate("zzzzz", "abcde"), [None, None, None, None, None])
        self.assertEqual(guess.evaluate("bbaac", "aabbc"), [False, False, False, False, True])

    def test_prune(self):
        """Test pruning."""
        self.assertEqual(set(guess.prune_candidates(
            [None, True, True, True, True],
            "clang",
            ["facts", "testy", "words", "blank", "blang", "bland", "clamp", "clang"]
        )), set(["blang"]))

        self.assertEqual(set(guess.prune_candidates(
            [None, True, True, True, True],
            "cynic",
            ["facts", "testy", "words", "blank", "blang", "bland", "clamp", "clang"]
        )), set(["blang"]))
