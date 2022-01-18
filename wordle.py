import random
import words
from collections import Counter
from enum import Enum
import argparse
from math import inf

WORDLE_SIZE = 5
DEFAULT_MAX_GUESSES = 6

class Status(Enum):
  present = 0
  correct = 1
  absent  = 2

Symbols = {
  Status.correct: "🟩",
  Status.present: "🟨",
  Status.absent: "⬜"
}

class Guess:
  def __init__(self, word, goal, candidates = words.mystery_words):
    self.goal = goal
    self.candidates = candidates
    self.word = word if word != None else self.best_guess()
    self.corrects = set()
    self.presents = set()
    self.evaluation = []

  def valid(self):
    return len(self.word) == WORDLE_SIZE and self.word.isalpha() and (self.word in words.legal_words or self.word in words.mystery_words)

  def evaluate(self, guess = None, goal = None):
    if len(self.word) != WORDLE_SIZE:
      return False

    guess = self.word if guess == None else guess
    goal = self.goal if goal == None else goal

    self.evaluation     = [Status.absent] * WORDLE_SIZE
    self.corrects = set()
    self.presents = set()
    guess_letter_open   = [True] * WORDLE_SIZE
    mystery_letter_open = [True] * WORDLE_SIZE

    # Find correct letters
    for i in range(len(self.evaluation)):
      if guess[i] == goal[i]:
        self.evaluation[i] = Status.correct
        guess_letter_open[i] = False
        mystery_letter_open[i] = False
        self.corrects.add(guess[i])

    # Find present letters
    for i in range(len(guess)):
      guess_letter = guess[i]
      if guess_letter_open[i]:
        for j in range(len(goal)):
          mystery_letter = goal[j]
          if mystery_letter_open[j] and mystery_letter == guess_letter:
            self.evaluation[i] = Status.present
            mystery_letter_open[j] = False
            self.presents.add(guess_letter)

    return self.evaluation == [Status.correct] * WORDLE_SIZE

  def prune_candidates(self):
    for i in range(len(self.evaluation)):
      if self.evaluation[i] == Status.correct:
        self.candidates = [word for word in self.candidates if word[i] == self.word[i]]
      elif self.evaluation[i] == Status.present:
        self.candidates = [word for word in self.candidates if self.word[i] in word and self.word[i] != word[i]]
      else:
        self.candidates = [word for word in self.candidates if ((self.word[i] != word[i]) and (self.word[i] not in word or self.word[i] in self.corrects or self.word[i] in self.presents))]

  def next(self):
    guess_scores = Counter()

    for guess in words.mystery_words + words.legal_words:
      hit_counts = Counter()
      score = inf

      for target in self.candidates:
        self.evaluate(guess, target)
        hit_counts.update([tuple(self.evaluation)])
        score = min(score, len(self.candidates) - hit_counts[tuple(self.evaluation)])

      guess_scores[guess] = score

    max = guess_scores.most_common(1)[0]
    max_score = max[1]

    cands = [cand for cand in self.candidates if guess_scores[cand] == max_score]

    result = cands[0] if len(cands) > 0 else max[0]
    self.word = result
    self.evaluate()
    self.prune_candidates()

  def __repr__(self):
    success = self.evaluate()
    evaluation_string = "".join([Symbols[l] for l in self.evaluation])
    return f"{evaluation_string} ({self.word}) {'Success!' if success else ''}"

class Wordle:
  def __init__(self, seed = ""):
    self.mystery_word = random.choice(words.mystery_words) if seed == "" else seed

  def play(self, max_guesses = DEFAULT_MAX_GUESSES):
    guesses = 0

    while guesses < max_guesses:
      guess = Guess(input("Enter guess: ").lower(), self.mystery_word, None)
      print ("\033[A                             \033[A")

      if guess.valid():
        guesses += 1
        success = guess.evaluate()
        print(guess)

        if success:
          return

    print(f"\nFailed... the wordle was '{self.mystery_word}'.")

  def solve(self, should_print=False):
    guesses = 0
    guess = Guess("soare", self.mystery_word)
    guess.evaluate()
    guess.prune_candidates()

    # Infinite loops aren't infinite to successful solvers...
    while True:
      guesses += 1
      success = guess.evaluate()

      if should_print:
        print(guess)

      if success:
        return guesses, self.mystery_word

      guess.next()

def run_solve(max_guesses = DEFAULT_MAX_GUESSES):
  solves = Counter()
  fails = set()

  for seed in words.mystery_words:
    solution = Wordle(seed).solve()
    solves.update([solution[0]])

    if solution[0] > max_guesses:
      fails.add(solution[1])

  print(solves)
  print(f"Failed words: {fails}")

def run_solve_on_seed(seed):
  if seed != "":
    Wordle(seed).solve(True)

def run_play(seed):
  wordle = Wordle(seed)
  wordle.play()

def main(args):
  if args.manual:
    run_play(args.seed)
  elif args.seed != "":
    run_solve_on_seed(args.seed)
  else:
    run_solve()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='play or solve wordle')
  parser.add_argument('--manual', action="store_true", help='play manually')
  parser.add_argument('--seed', default="", type=str, help='seed word')
  main(parser.parse_args())
