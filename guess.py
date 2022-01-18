from collections import Counter
from enum import Enum
from math import inf
import words

WORDLE_SIZE = 5

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
    self.word = word
    self.corrects = set()
    self.presents = set()
    self.evaluation = []
    self.succesful = self.evaluate()
    self.prune_candidates()

  def valid(self):
    return len(self.word) == WORDLE_SIZE and self.word.isalpha() and (self.word in words.legal_words or self.word in words.mystery_words)

  def successful(self):
    return self.succesful

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
    self.succesful = self.evaluate()
    self.prune_candidates()

  def __repr__(self):
    success = self.evaluate()
    evaluation_string = "".join([Symbols[l] for l in self.evaluation])
    return f"{evaluation_string} ({self.word}) {'Success!' if success else ''}"