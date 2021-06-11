import random

# Global Variables (Yes I know this is bad style but I'm LAZY)
guesses = 0
guessed_letters = set()
word = ''
cash = 0
prize = False
prize_text = "An all-expenses-paid trip to your local motel!"

# Unicode for our hangman image
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

vowels = ['a', 'e', 'i', 'o', 'u']
# Tracks whether all vowels have been guessed
all_vowels = False

# All of our possible results!
wheel = {0: "Bankrupt", 1:"Loss", 2:200, 3:250, 4:300, 5:300, 6:350, 7:350, 8:400, 9:400, 10:450, 11:"Gamble",
         12:"Free", 13:450, 14:500, 15:500, 16:550, 17:550, 18:600, 19:600, 20:700, 21:750, 22:"Prize", 23:"Jackpot"}

# A guessing game is no fun if the word is 'hi'
# It's also no fun if you've never heard of that word before
# This file contains words from the top 10,000 english words, filtered by length from this word set
# Original list source: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
def make_wordlist():
    success = False
    infile = open('words.txt')
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

def input_vowel():
    global all_vowels
    guess = input("Guess a vowel! ")
    if not guess.isalpha() or guess not in vowels:
        print("\nError: Please enter a single vowel!\n")
        return input_vowel()
    if guess in guessed_letters:
        print("\nError: You already guessed that letter! Try a new guess.\n")
        return input_vowel()

    guess = guess.lower()
    guessed_letters.add(guess)

    # Determine whether all vowels have been guessed
    check_v = True
    for vowel in vowels:
        if vowel not in guessed_letters:
            check_v = False
    all_vowels = check_v
    return guess
    
def input_consonant():
    guess = input("Guess a consonant! ")
    if not guess.isalpha() or guess in vowels:
        print("\nError: Please enter a single consonant!\n")
        return input_consonant()
    if guess in guessed_letters:
        print("\nError: You already guessed that letter! Try a new guess.\n")
        return input_consonant()

    guess = guess.lower()
    guessed_letters.add(guess)
    
    return guess

def check_victory():
    for letter in word:
        if letter not in guessed_letters:
            return 0
    return 1
    

# Returns 1 for win, -1 for loss, or 0 to continue playing
def turn():
    global guesses, cash, prize
    # Return value
    result = 0

    # Display current game status
    print('\n\n\n')
    print(f'Guesses Left: {7 - guesses}', end = '')

    print(status[guesses])

    print(f"\nYour total ${cash}\n")
    
    
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

    # Spin the wheel!
    print("Let's spin the wheel!\n")
    roll = wheel[random.randint(0,23)]

    if roll == "Bankrupt":
        print("Oh no! You've gone bankrupt! Better luck next spin!\n")
        cash = 0
        # If they go bankrupt, they don't get to do anything else this turn

        input("Press enter to continue to the next turn. ")
        return 0

    elif roll == "Loss":
        print("Bad luck! Guess a letter correctly or lose $1000!\n")
        guess = input_consonant()
    
        if guess not in word:
            print(f"Oh no! {guess.upper()} is not in the word! You lose $1000\n")
            cash -= 1000
            guesses += 1
        else:
            count = word.count(guess)
            if count == 1:
                print(f"Nice! There is 1 {guess} in the word! You can keep your money!\n")
            else:
                print(f"Nice! There are {count} {guess}s in the word! You can keep your money!\n")
            result = check_victory()

    elif roll == "Gamble":
        print("You rolled a mystery! You can play for $500, or make a gamble!\n \
If you gamble, theres a 50% chance of getting a $5000 jackpot, and a 50% chance of going bankrupt.\n")
        choice = input("Would you like to gamble? Enter Y to take the chance, or N to play for $500 ")
        if choice.lower() == 'y':
            lucky = random.randint(0,1)
            if lucky:
                print("Congratulations, it's your lucky day! You win $5000\n")
                cash += 5000

                input("\nPress enter to continue to the next turn. ")
                return 0
            else:
                print("Oh no! You've gone bankrupt...\n")
                cash = 0

                input("\nPress enter to continue to the next turn. ")
                return 0
            # Either gamble result moves to the next turn
            
        else:
            print("Taking the safe route, I see. Well, then...")
            guess = input_consonant()
            
            if guess in word:
                count = word.count(guess)
                if count == 1:
                    print(f"\nNice! There is 1 {guess} in the word! You win $500!\n")
                else:
                    print(f"\nNice! There are {count} {guess}s in the word! You win ${count*500}!\n")
                cash += count * 500
                result = check_victory()    
            else:
                print(f"\nOoh, too bad! {guess} is not in the word!\n")
                guesses += 1
    
    elif roll == "Free":
        if not all_vowels:
            print("Congrats, you can get a free vowel! If you don't want a free vowel, you can buy a consonant for $250")
            valid = False
            while not valid:
                response = input("Would you like a free vowel, or do you want to buy a consonant? Enter V for vowel or C for consonant. ")
                if response.lower() != 'v' and response.lower() != 'c':
                    print("Error: Response not recognized. Please try again.")
                else:
                    valid = True
            if response == 'v':
                guess = input_vowel()

                if guess in word:
                    count = word.count(guess)
                    if count == 1:
                        print(f"\nNice! There is 1 {guess} in the word!\n")
                    else:
                        print(f"\nNice! There are {count} {guess}s in the word!\n")
                    result = check_victory()    
                else:
                    print(f"\nOoh, too bad! {guess} is not in the word!\n")
                    
            elif response == 'c':
                cash -= 250
                guess = input_consonant()
                
                if guess in word:
                    count = word.count(guess)
                    if count == 1:
                        print(f"\nNice! There is 1 {guess} in the word!\n")
                    else:
                        print(f"\nNice! There are {count} {guess}s in the word!\n")
                    result = check_victory()    
                else:
                    print(f"\nOoh, too bad! {guess} is not in the word!\n")

            input("\nPress enter to continue to the next turn. ")
            return result
        else:
            print("Congrats, you can get a free vowel... but all the vowels have been guessed!")
            print("As a consolation prize, have $1000, on us")
            cash += 1000
            input("\nPress enter to continue to the next turn. ")
            return 0
            
    elif roll == "Prize":
        print("Congratulations, you've won an excellent prize! Your prize is:")
        print(f"{prize_text}\n")
        prize = True
        
        input("\nPress enter to continue to the next turn. ")
        return 0

    elif roll == "Jackpot":
        print("CONGRATULATIONS!! You hit the big jackpot! You just won $5000!\n")
        cash += 5000

        input("\nPress enter to continue to the next turn. ")
        return 0
        
    else:
        print(f"You rolled ${roll}! Let's play!\n")
        
        guess = input_consonant()

        if guess in word:
            count = word.count(guess)
            if count == 1:
                print(f"\nNice! There is 1 {guess} in the word! You win ${roll}!\n")
            else:
                print(f"\nNice! There are {count} {guess}s in the word! You win ${count*roll}!\n")
            result = check_victory()
            cash += count * roll
        else:
            print(f"\nOoh, too bad! {guess} is not in the word!\n")
            guesses += 1

    if result:
        return 1
    
    # Buy a vowel... if they haven't all been guessed
    vowel = 'n'
    if not all_vowels:
        print("Word:", end = ' ')
        for letter in word:
            if letter in guessed_letters:
                print(letter, end=' ')
            else:
                print('_', end=' ')
        print(f"\n\nYour total ${cash}\n")
        
        vowel = input("Would you like to buy a vowel for $250? Enter Y to buy a vowel ").lower()
    while vowel == 'y' and not all_vowels:
        cash -= 250
        guess = input_vowel()
        
        if guess in word:
            count = word.count(guess)
            if count == 1:
                print(f"Nice! There is 1 {guess} in the word!\n")
            else:
                print(f"Nice! There are {count} {guess}s in the word!\n")
            result = check_victory()    
        else:
            print(f"Ooh, too bad! {guess} is not in the word!\n")
        if not all_vowels:
            print("Word:", end = ' ')
            for letter in word:
                if letter in guessed_letters:
                    print(letter, end=' ')
                else:
                    print('_', end=' ')
            print(f"\n\nYour total ${cash}\n")
            vowel = input("Would you like to buy another vowel for $250? Enter Y to buy a vowel ").lower()

    # Guess the whole word, if you dare
    print("\n\n")
    print("Word:", end = ' ')
    for letter in word:
        if letter in guessed_letters:
            print(letter, end=' ')
        else:
            print('_', end=' ')
    if guesses >= 7:
        print("\nThis is your last chance!")
    if input("\nWould you like to try to guess the word? Enter Y to make a guess. ").lower() == 'y':
        guess = input("Well then, let's hear it! Guess the word: ").lower()
        if guess == word:
            print("\n...\n\nThat's it! You got it!\n")
            return 1
        else:
            guesses -= 1
            print("\nI'm sorry, but that is not the word.\n")

    if guesses >= 7:
         result = -1

    input("\nPress enter to continue to the next turn. ")
    return result

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
    print(f"\nYou ended the game with ${cash}!")
    if cash < 0:
        print("Looks like you owe us some money!")
    if prize and result == 1:
        print(f"You also won our excellent prize: {prize_text}! How wonderful!")
    print(f"\nYour Record: {wins} Wins, {losses} Losses")
    
    if input("\nWould you like to play again? (Enter Y to Replay) ").lower() == 'y':
        play(wins, losses)
    else:
        print("\nThank you for playing!")
        return

print("Welcome to Wheel of Fortune!\n")

words = make_wordlist()

play(0,0)

