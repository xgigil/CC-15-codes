
# Word Count
words = input("Enter Word:")
print ("The word is " + words)

wordCount = len(words.split())
print(f"Number of words: {wordCount}")

# Vowels
vowels = "aeiouAEIOU"

vowelCount = sum(words.count(vowel) for vowel in vowels)
print(f"Number of vowels: {vowelCount}")

# Frequency
new_text = words.replace(" ", "").lower()

characters = []
frequency = []

for char in new_text:
    if char in characters:

         index = characters.index(char)
         frequency[index] += 1
    else:

         characters.append(char)
         frequency.append(1)

print("Character Frequency:")
for i in range(len(characters)):
    print(f"'{characters[i]}': {frequency[i]}")

# Palindrome


if  new_text == new_text[::-1]:
    print("The String is a palindrome.")
else:
    print("The String is not a palindrome.")

# Reversed
new_text = new_text[::-1]
print(f"Reversed String: {words}")








