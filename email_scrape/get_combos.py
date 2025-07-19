#Generate all possible combinations of vowel/consonant/vowel strings
vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'
combinations = []
for vowel1 in vowels:
  for consonant in consonants:
    for vowel2 in vowels:
      combinations.append(f'{vowel1}{consonant}{vowel2}')
with open('combinations.txt', 'w') as f:
  for combo in combinations:
    f.write(combo + '\n')
