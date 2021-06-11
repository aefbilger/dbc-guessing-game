import random

# Global Variables (Yes I know this is bad style but I'm LAZY)
guesses = 0
guessed_letters = set()
word = ''

# Unicode images for our hangman image
status = {0:
          '''
_____
|   |
|
|
|
|
----------
''',
          1:
          '''
_____
|   |
|   o
|
|
|
----------
''',
          2:
          '''
_____
|   |
|   o
|   |
|
|
----------
''',
          3:
          '''
_____
|   |
|   o
|  /|
|
|
----------
''',
          4:
          r'''
_____
|   |
|   o
|  /|\
|
|
----------
''',
          5:
          r'''
_____
|   |
|   o
|  /|\
|  /
|
----------
''',
          6:
          r'''
_____
|   |
|   o
|  /|\
|  / \
|
----------
''',
          7:
          r'''
_____
|   |
|   x
|  /|\
|  / \
|
----------
'''
          }

# A guessing game is no fun if the word is 'hi'
# It's also no fun if you've never heard of that word before
# This file contains words from the top 10,000 english words, filtered by length from this word set
# Original list source: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
def make_wordlist():
    success = False
    infile = open('somewords.txt')
    words_raw = infile.read().splitlines()
    infile.close()
    while not success:
        try:
            words = []
            length = int(input("Please choose a minimum word length for this game. (Note: At least 6 is recommended!) "))
            if length < 1:
                print("\nError: Please enter a positive integer for length!\n")
            else:
                for word in words_raw:
                    if len(word) >= length:
                        words.append(word)
                if len(words) == 0:
                    print("\nError: Oops! There are no words of that length. Please enter a smaller number.\n")
                else:
                    infile.close()
                    return words
        except ValueError:
            print("\nError: Please enter a positive integer for length!\n")

    return None
             

# Setup for each round of play
def init():
    global word, guesses, guessed_letters
    guesses = 0
    guessed_letters = set()
    
    word = random.choice(words)
    # No duplicate words in successive rounds
    words.remove(word)
    # To keep things (case) insensitive
    word = word.lower()


def user_input():
    guess = input("Guess a letter, or try to guess the whole word! ")
    if not guess.isalpha():
        print("\nError: Please enter a letter or a word!\n")
        return user_input()
    if guess in guessed_letters:
        print("\nError: You already guessed that letter! Try a new guess.\n")
        return user_input()
    return guess


# Returns 1 for win, -1 for loss, or 0 to continue playing
def turn():
    global guesses
    # Display current game status
    print('\n\n\n')
    print(f'Guesses Left: {7 - guesses}', end = '')

    print(status[guesses])

    print("Word:", end = ' ')
    for letter in word:
        if letter in guessed_letters:
            print(letter, end=' ')
        else:
            print('_', end=' ')
    print('\n')
    
    print("Previous guesses:", end = ' ')
    for letter in guessed_letters:
        print(letter.lower(), end=' ')
    print('\n')

    guess = user_input()

    # If the user guessed a word
    if len(guess) > 1:
        if guess == word:
            return 1
        else:
            guesses += 1

    # If the user guessed a letter
    else:
        guess = guess.lower()
        guessed_letters.add(guess)
        
        if guess in word:
            # Check if all letters have been guessed
            victory = True
            for letter in word:
                if letter not in guessed_letters:
                    victory = False
            if victory:
                return 1
        else:
            guesses += 1

    if guesses < 7:
        return 0
    return -1


def play(wins, losses):
    init()
    result = 0

    while result == 0:
        result = turn()

    print('\n\n\n')
    
    if result == 1:
        wins += 1
        print("You win!")
    elif result == -1:
        losses += 1
        print(status[7])
        print(f"The word was {word}\n")
        print("You lose... :(")

    print(f"\nYour Record: {wins} Wins, {losses} Losses")
    if input("\nWould you like to play again? (Enter Y to Replay) ").lower() == 'y':
        play(wins, losses)
    else:
        print("\nThank you for playing!")
        return

print("Welcome to the guessing game!\n")

words = make_wordlist()

play(0,0)

