"""Wordle."""

import argparse
from ast import Raise
from collections import Counter
from multiprocessing.sharedctypes import Value
import random

from guess import CORRECT_GUESS, Guess, evaluate, valid, prune_candidates
import words

DEFAULT_MAX_GUESSES = 6

class Game:
    """Representation of a game of Wordle.
        Games may be played by the user or solved by the program."""

    def __init__(self, seed = None):
        """Initialize a wordle game, with a random starting word if none is given."""
        self.mystery_word = random.choice(words.mystery_words) if seed is None else seed

    def play(self, verbose=False, max_guesses = DEFAULT_MAX_GUESSES):
        """Plays a game of wordle."""
        guesses = 0
        guess = Guess("", self.mystery_word, words.mystery_words)

        while guesses < max_guesses:
            guess.word = input("Enter guess: ").lower()
            print ("\033[A                             \033[A") # hack for shell

            if valid(guess.word):
                guesses += 1
                print(guess)

                if evaluate(guess.word, guess.goal) == CORRECT_GUESS:
                    return

                guess.take_guess(guess.word)

                if verbose:
                    print(guess.candidates)

        print(f"\nFailed... the wordle was '{self.mystery_word}'.")

    def solve(self, verbose=False):
        """Solves a game of wordle."""
        guesses = 0

        guess = Guess(None, self.mystery_word, words.mystery_words)

        while True:
            guesses += 1

            if verbose:
                print(guess)

            if evaluate(guess.word, guess.goal) == CORRECT_GUESS:
                return guesses, self.mystery_word

            if verbose:
                print(guess.candidates)

            guess.next_guess()

    @staticmethod
    def solve_all(max_guesses = DEFAULT_MAX_GUESSES):
        """Solves all posssible Wordles and outputs a counter of results."""
        solves = Counter()
        fails = set()

        for seed in words.mystery_words:
            solution = Game(seed).solve()
            solves.update([solution[0]])

            if solution[0] > max_guesses:
                fails.add(solution[1])

        print(solves)
        print(f"Failed words: {fails}")

class SeedAction(argparse.Action):
    """Validates a seed."""
    def __call__(self, parser, namespace, values, option_string=None):
        """If a seed is not in mystery_words, it is invalid."""
        if values not in words.mystery_words:
            raise ValueError("Not a valid seed!")
        setattr(namespace, self.dest, values)

def main(args):
    """Run Wordle."""
    if args.manual:
        Game(args.seed).play(args.candidates)
    elif args.seed is not None:
        Game(args.seed).solve(True)
    else:
        Game.solve_all()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='play or solve wordle')
    parser.add_argument('--manual', action="store_true", help='play manually')
    parser.add_argument('--seed', default=None, action=SeedAction, type=str, help='seed word')
    parser.add_argument('--candidates', action="store_true", help="view candidates")
    main(parser.parse_args())
