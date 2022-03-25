"""Guess."""

from collections import Counter
from math import inf
from joblib import Memory
import words

WORDLE_SIZE = 5
CORRECT_GUESS = [True] * WORDLE_SIZE

# Cache our suggestions to disk to drastically improve run-time.
memory = Memory("cache/", verbose=0)

def valid(guess):
    """Returns whether the guess was valid."""
    return len(guess) == WORDLE_SIZE and guess.isalpha() and (guess
        in words.legal_words or guess in words.mystery_words)

def evaluate(guess, goal):
    """Evaluate a guess according to the goal word. 'Corrects' are represented by
        True, 'Presents' by False, and 'Absents' by None."""
    evaluation = [None] * WORDLE_SIZE
    guess = list(guess)
    goal = list(goal)

    # Find correct letters
    for i in range(WORDLE_SIZE):
        if guess[i] == goal[i]:
            evaluation[i] = True
            guess[i] = None
            goal[i] = None

    # Find present letters
    for i in range(WORDLE_SIZE):
        guess_letter = guess[i]
        if guess[i] is not None:
            for j in range(WORDLE_SIZE):
                mystery_letter = goal[j]
                if mystery_letter == guess_letter:
                    evaluation[i] = False
                    goal[j] = None
                    break

    return evaluation

def prune_candidates(evaluation, guess, candidates):
    """Prunes candidates according to the given evaluation."""
    corrects = [letter for letter, value in zip(guess, evaluation) if value]
    presents = [letter for letter, value in zip(guess, evaluation) if (value
        is not None and not value)]

    for i, value in enumerate(evaluation):
        if value is None:
            candidates = [cand for cand in candidates if ((guess[i] != cand[i])
                and (guess[i] not in cand or guess[i] in corrects or guess[i] in presents))]
        elif value:
            candidates = [cand for cand in candidates if cand[i] == guess[i]]
        else:
            candidates = [cand for cand in candidates if guess[i] in cand and guess[i] != cand[i]]

    return candidates

@memory.cache
def make_suggestion(candidates):
    """Makes a suggestion based upon the possible candidates."""
    guess_scores = Counter()
    cand_len = len(candidates)

    for guess in words.mystery_words + words.legal_words:
        hit_counts = Counter()
        score = inf

        for target in candidates:
            evaluation = evaluate(guess, target)
            hashed = tuple(evaluation)
            hit_counts[hashed] += 1
            score = min(score, cand_len - hit_counts[hashed])

        guess_scores[guess] = score

    max_item = guess_scores.most_common(1)[0]
    max_score = max_item[1]

    cands = [cand for cand in candidates if guess_scores[cand] == max_score]

    return cands[0] if len(cands) > 0 else max_item[0]

class Guess:
    """A wordle guess, consisting of a guess word,
        the goal word, and the remaining candidates."""

    def __init__(self, word, goal, candidates):
        """Initialize a guess."""
        self.goal = goal
        self.word = word
        self.candidates = candidates

        if self.word is None:
            self.next_guess()

    def next_guess(self):
        """Make the next best guess."""
        self.word = make_suggestion(self.candidates)
        evaluation = evaluate(self.word, self.goal)
        self.candidates = prune_candidates(evaluation, self.word, self.candidates)

    def __repr__(self):
        """Returns the symbolic representation of the guess."""
        symbol_map = {
            None: "⬜",
            True: "🟩",
            False: "🟨"
        }

        evaluation = evaluate(self.word, self.goal)
        string = "".join([symbol_map[l] for l in evaluation])
        return f"{string} ({self.word}) {'Success!' if evaluation == CORRECT_GUESS else ''}"
