def generate_guess(frequencies, previously_used = set()):
  return sort_guesses(frequencies, words.mystery_words, previously_used)




class IndexLetterFrequencyMap:
  def __init__(self):
    self.map = dict()

    for index in range(5):
      self.map[index] = dict()
      for letter in "abcdefghijklmnopqrstuvwxyz":
        self.map[index][letter] = 0

  def __repr__(self) -> str:
    output = ""
    for index in self.map.items():
      output += "\n\n"
      sorted = list(index[1].items())
      sorted.sort(reverse=True, key=lambda item : item[1])

      for key, value in sorted:
        output += key + " " + str(value) + "\n"

    return output

  def add(self, word):
    for i in range(len(word)):
      self.map[i][word[i]] += 1


def letter_split_frequencies_from_source(source):
  freqMap = IndexLetterFrequencyMap()

  for word in source:
    freqMap.add(word)

  return freqMap

def letter_split_frequencies():
  return letter_split_frequencies_from_source(words.mystery_words)

def sort_split_guesses(frequencies, guesses):
  scores = dict()

  for word in guesses:
    score = 0
    for index in range(len(word)):
      score += frequencies.map[index][word[index]]
    scores[word] = score

  sorted = list(scores.items())
  sorted.sort(reverse=True, key=lambda item : item[1])

  return sorted

def generate_split_guess(frequencies):
  return sort_split_guesses(frequencies, words.mystery_words)
