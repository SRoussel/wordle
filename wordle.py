import random
import words
import os
from collections import Counter

class LetterFrequencyMap:
  def __init__(self, source):
    self.map = dict()

    for word in source:
      self.add(word)

  def __repr__(self) -> str:
    output = ""
    sorted = list(self.map.items())
    sorted.sort(reverse=True, key=lambda item : item[1])

    for key, value in sorted:
      output += key + " " + str(value) + "\n"

    return output

  def add(self, word):
    for letter in set(list(word)):
      if letter in self.map:
        self.map[letter] += 1
      else:
        self.map[letter] = 1

PRESENT = 0
CORRECT = 1
ABSENT  = 2

symbols = {
  CORRECT: "🟩",
  PRESENT: "🟨",
  ABSENT: "⬜"
}

class Wordle:
  def __init__(self, seed = ""):
    self.mystery_word = Wordle.random_word() if seed == "" else seed
    self.candidates = words.mystery_words
    self.frequencies = LetterFrequencyMap(words.mystery_words)

  def evaluate(self, guess):
    if len(guess) != 5 or self.mystery_word == None:
      return None

    evaluation          = [ABSENT] * 5
    guess_letter_open   = [True] * 5
    mystery_letter_open = [True] * 5

    # Find correct letters
    for i in range(len(evaluation)):
      if guess[i] == self.mystery_word[i]:
        evaluation[i] = CORRECT
        guess_letter_open[i] = False
        mystery_letter_open[i] = False

    # Find present letters
    for i in range(len(guess)):
      guess_letter = guess[i]
      if guess_letter_open[i]:
        for j in range(len(self.mystery_word)):
          mystery_letter = self.mystery_word[j]
          if mystery_letter_open[j] and mystery_letter == guess_letter:
            evaluation[i] = PRESENT
            mystery_letter_open[j] = False

    corrects = set()
    presents = set()
    for i in range(len(evaluation)):
      if evaluation[i] == CORRECT:
        corrects.add(guess[i])
      elif evaluation[i] == PRESENT:
        presents.add(guess[i])

    for i in range(len(evaluation)):
      if evaluation[i] == CORRECT:
        self.candidates = [word for word in self.candidates if word[i] == guess[i]]
      elif evaluation[i] == PRESENT:
        self.candidates = [word for word in self.candidates if guess[i] in word and guess[i] != word[i]]
      else:
        self.candidates = [word for word in self.candidates if ((guess[i] != word[i]) and (guess[i] not in word or guess[i] in corrects or guess[i] in presents))]

    self.frequencies = LetterFrequencyMap(self.candidates)
    guesses = sort_guesses(self.frequencies, self.candidates)
    #print(guesses)
    return evaluation, guesses[0][0]

  def print_evaluation(self, guess):
    evaluation, suggestion = self.evaluate(guess)
    evaluation_string = "".join([symbols[l] for l in evaluation])
    print(f"{evaluation_string} ({guess})")
    return evaluation, suggestion

  def random_word():
    return random.choice(words.mystery_words)

  def play(self):
    guesses = 0

    while guesses < 6:
      guess = input("Enter guess: ").lower()
      print ("\033[A                             \033[A")

      if (len(guess) == 5 and guess.isalpha() and (guess in words.legal_words or guess in words.mystery_words)):
        guesses += 1

        if self.print_evaluation(guess)[0] == [CORRECT] * 5:
          print("Success!")
          return

    print(f"\nFailed... the wordle was '{self.mystery_word}'.")

  def solve(self):
    guesses = 0
    guess = sort_guesses(self.frequencies, self.candidates)[0][0]

    # Infinite loops aren't infinite to successful solvers...
    while True:
      guesses += 1

      success, guess = self.print_evaluation(guess)
      if success == [CORRECT] * 5:
        return guesses, self.mystery_word

def sort_guesses(frequencies, guesses):
  scores = dict()

  for word in guesses:
    used = set()
    score = 0
    for letter in word:
      if letter not in used:
        score += frequencies.map[letter]
        used.add(letter)
    scores[word] = score

  sorted = list(scores.items())
  sorted.sort(reverse=True, key=lambda item : item[1])
  return sorted

def run_solve():
  solves = dict()
  fails = set()

  for seed in words.mystery_words:
    wordle = Wordle(seed)
    solution = wordle.solve()

    if solution[0] in solves:
      solves[solution[0]] += 1
    else:
      solves[solution[0]] = 1

    if solution[0] > 6:
      fails.add(solution[1])

  if -1 in solves:
    print(f"Failed: {solves[-1]}")

  solutions = list(solves.items())
  solutions.sort()

  for num_guesses, num_words in solutions:
    print(f"Solved in {num_guesses}: {num_words}")

  print(f"Failed words: {fails}")

def run_play():
  wordle = Wordle()
  wordle.play()

def main():
  run_solve()
  #run_play()
  #wordle = Wordle("homer")
  #wordle.solve()

if __name__ == "__main__":
  main()
