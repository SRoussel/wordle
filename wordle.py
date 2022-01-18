import argparse
from collections import Counter
import random

from guess import Guess
import words

DEFAULT_MAX_GUESSES = 6

class Wordle:
  def __init__(self, seed = ""):
    self.mystery_word = random.choice(words.mystery_words) if seed == "" else seed

  def play(self, max_guesses = DEFAULT_MAX_GUESSES):
    guesses = 0

    while guesses < max_guesses:
      guess = Guess(input("Enter guess: ").lower(), self.mystery_word)
      print ("\033[A                             \033[A")

      if guess.valid():
        guesses += 1
        print(guess)

        if guess.successful():
          return

    print(f"\nFailed... the wordle was '{self.mystery_word}'.")

  def solve(self, should_print=False):
    guesses = 0

    # This would take a while to calculate...
    guess = Guess("soare", self.mystery_word)

    while True:
      guesses += 1

      if should_print:
        print(guess)

      if guess.successful():
        return guesses, self.mystery_word

      guess.next()

  def solve_all(max_guesses = DEFAULT_MAX_GUESSES):
    solves = Counter()
    fails = set()

    for seed in words.mystery_words:
      solution = Wordle(seed).solve()
      solves.update([solution[0]])

      if solution[0] > max_guesses:
        fails.add(solution[1])

    print(solves)
    print(f"Failed words: {fails}")

def main(args):
  if args.manual:
    Wordle(args.seed).play()
  elif args.seed != "":
    Wordle(args.seed).solve(True)
  else:
    Wordle.solve_all()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='play or solve wordle')
  parser.add_argument('--manual', action="store_true", help='play manually')
  parser.add_argument('--seed', default="", type=str, help='seed word')
  main(parser.parse_args())
