from random import randint

number = randint(1, 100)
levels = ["Easy", "Medium", "Hard"]
chances = [10, 5, 3]

print("""Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
You have a limited number of chances to guess the corrent number.

Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)
""")

while True:
    try:
        difficulty = int(input("Enter you choice (1-3): "))
        if 1 <= difficulty <= 3:
            break
        else:
            print("Please enter a number between 1 and 3.")
    except ValueError:
        print("Invalid input")

print(f"""
Great! You have selected the {levels[difficulty - 1]} difficulty level.
Let's start the game!
""")

for attempts in range(chances[difficulty - 1]):
    while True:
        try:
            guess = int(input("Enter you guess (1-100): "))
            if 1 <= guess <= 100:
                break
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input")

    if guess == number:
        print(
            f"Congratulations! You guessed the correct number in {attempts + 1} attempts.",
            end=2 * "\n",
        )
        break

    if guess < number:
        print(f"Incorrect! The number is greater than {guess}", end=2 * "\n")

    else:
        print(f"Incorrect! The number is less than {guess}", end=2 * "\n")

print(f"Game over! The correct number was {number}")
