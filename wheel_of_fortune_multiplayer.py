import random

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

# Initializes a full play session
def init():
    global words
    words = make_wordlist()

    create_players()

def create_players():
    global players
    
    valid = False
    while not valid:
        player_count = input("How many players? ")
        if not player_count.isnumeric():
            print("Error: Please enter a number!")
        player_count = int(player_count)
        if player_count <= 0:
            print("Error: You need to have a positive number of players!")
        elif player_count == 1:
            print("This is a multiplayer game. If you want to play alone, try our single-player version!")
        else:
            valid = True
    for i in range(player_count):
        player_dict = {}
        player_dict['name'] = input(f"Player {i+1}, what is your name? ")
        player_dict['cash'] = 0
        player_dict['wins'] = 0
        player_dict['prize'] = False
        print(player_dict)
        players.append(player_dict)
    print(players)
    

# Setup for each round of play
def setup():
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
    

# Returns 1 for win, 0 to play another turn with the same player, and -1 to continue to the next player
def turn(player):
    global players, prize
    # Return value
    result = 0
    
    # Display current game status
    print('\n\n\n')
    
    print(f"{players[player]['name']}, it's your turn!\n")
    print(f"\nYour total ${players[player]['cash']}\n")
    
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
        players[player]['cash'] = 0
        
        # If they go bankrupt, they don't get to do anything, and we skip to the next player
        input("Press enter to continue to the next turn. ")
        return -1

    elif roll == "Loss":
        print("Bad luck! Guess a letter correctly or lose $1000!\n")
        guess = input_consonant()
    
        if guess not in word:
            print(f"Oh no! {guess.upper()} is not in the word! You lose $1000\n")
            players[player]['cash'] -= 1000
            input("Press enter to continue to the next turn. ")
            return -1
        else:
            count = word.count(guess)
            if count == 1:
                print(f"Nice! There is 1 {guess} in the word! You can keep your money!\n")
            else:
                print(f"Nice! There are {count} {guess}s in the word! You can keep your money... For now.\n")
            result = check_victory()

    elif roll == "Gamble":
        print("You rolled a mystery! You can play for $500, or make a gamble!\n \
If you gamble, theres a 50% chance of getting a $5000 jackpot, and a 50% chance of going bankrupt.\n")
        choice = input("Would you like to gamble? Enter Y to take the chance, or N to play for $500 ")
        if choice.lower() == 'y':
            lucky = random.randint(0,1)
            if lucky:
                print("Congratulations, it's your lucky day! You win $5000\n")
                players[player]['cash'] += 5000

                input("\nPress enter to continue to the next turn. ")
                return 0
            else:
                print("Oh no! You've gone bankrupt...\n")
                players[player]['cash'] = 0

                input("\nPress enter to continue to the next turn. ")
                return -1
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
                players[player]['cash'] += count * 500
                result = check_victory()    
            else:
                print(f"\nOoh, too bad! {guess} is not in the word!\n")
                return -1
    
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
            print("As a consolation prize, have $1000, on us.\n")
            players[player]['cash'] += 1000
            input("\nPress enter to continue to the next turn. ")
            return 0
            
    elif roll == "Prize":
        print("Congratulations, you've won an excellent prize! Your prize is:")
        print(f"{prize_text}\n")
        players[player]['prize'] = True
        
        input("\nPress enter to continue to the next turn. ")
        return 0

    elif roll == "Jackpot":
        print("CONGRATULATIONS!! You hit the big jackpot! You just won $5000!\n")
        players[player]['cash'] += 5000

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
            players[player]['cash'] += count * roll
        else:
            print(f"\nOoh, too bad! {guess} is not in the word!\n")
            return -1

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
        players[player]['cash'] -= 250
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
    if input("\nWould you like to try to guess the word? Enter Y to make a guess. ").lower() == 'y':
        guess = input("Well then, let's hear it! Guess the word: ").lower()
        if guess == word:
            print("\n...\n\nThat's it! You got it!\n")
            return 1
        else:
            print("\nI'm sorry, but that is not the word.\n")
            return -1

    input("\nPress enter to continue to the next turn. ")
    return result

def play():
    setup()
    result = 0
    # Start with player 1
    current_player = 0

    while result != 1:
        result = turn(current_player)
        if result == -1:
            current_player += 1
            if current_player >= len(players):
                current_player = 0

    print('\n\n\n')
    
    players[current_player]['wins'] += 1
    print(f"{players[current_player]['name']}, you win!")
    print(f"You get to take home an incredible ${players[current_player]['cash']} in cold, hard cash!")
    if players[current_player]['cash'] < 0:
        print("Oh, um.... it actually looks like you owe us some money.")
    if player[current_player]['prize']:
        print(f"In addition to your cash winnings, you also won our excellent prize: {prize_text}! How wonderful!")

    for player in players:
        print(f"\n{player['name'], you ended the game with ${player['cash']}!")
        if cash < 0:
            print("Looks like you owe us some money!")

    print("\nPlayer Records:")
    for player in players:
        if player['wins'] == 1:
            print(f"{player['name']: 1 win")
        else:
            print(f"{player['name']: player['wins']} wins")
    
    if input("\nWould you like to play again with the same players? (Enter Y to Replay) ").lower() == 'y':
        play()
    else:
        print("\nThank you for playing!")
        return

# Global Variables (Yes I know this is bad style but I'm LAZY)
guessed_letters = set()
word = ''
words = []

cash = 0

prize = False
prize_text = "A fun, romantic getaway for two, to IKEA, with a $200 budget!"

players = []

vowels = ['a', 'e', 'i', 'o', 'u']
# Tracks whether all vowels have been guessed
all_vowels = False

# All of our possible results!
wheel = {0: "Bankrupt", 1:"Loss", 2:200, 3:250, 4:300, 5:300, 6:350, 7:350, 8:400, 9:400, 10:450, 11:"Gamble",
         12:"Free", 13:450, 14:500, 15:500, 16:550, 17:550, 18:600, 19:600, 20:700, 21:750, 22:"Prize", 23:"Jackpot"}

print("Welcome to Wheel of Fortune, multiplayer edition!\n")

init()

play()

