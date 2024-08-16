from time import time, sleep
import random
import json


# Random Number Generator
lowX = 1
highX = 4


# Choose Game Mode
menu_options = ('p', 'l', 'x')


#########################
# LEADERBOARD FUNCTIONS #
#########################


# Load leaderboard
def load_leaderboard(filename='leaderboard.json'):
    try:
        with open(filename, 'r') as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = []
    return leaderboard

# Save leaderboard
def save_leaderboard(leaderboard, filename='leaderboard.json'):
    with open(filename, 'w') as file:
        json.dump(leaderboard, file, indent=4)

# Update leaderboard
def update_leaderboard(player_name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": player_name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)
    return leaderboard

# Display Leaderboard
def display_leaderboard():
    leaderboard = load_leaderboard()
    top_10 = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    
    print("Top 10 Leaderboard:")
    for idx, entry in enumerate(top_10, start=1):
        print(f"{idx}. {entry['name']} - {entry['score']} XP")
    
# Is the new score in the top ten?
def is_top_ten(leaderboard, player_name, score):
    top_10 = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    return {"name": player_name, "score": score} in top_10

player_name = None

###################
# START GAME MENU #
###################

while True:

    # Player Variables 
    lives = 3
    placeholder_xp = 0
    total_xp = 0
    level = 1
    lvlNext = 5

    print()
    print('****************************')
    print()
    print('WELCOME TO MULTIPICATION MADNESS')
    print()
    print('p = Play')
    print('l = View Leaderboard')
    print('x = Exit')
    print()
    print('****************************')

    # It will only ask for your name once until you exit the program
    if player_name is None:
        player_name = input("Please enter your name: ")

    mode = input("Please choose an option (Case-Sensitive): ")


    if mode == 'p':
        # PLAY GAME
        while lives > 0:

            # Your lucky numbers are..
            num1X = random.randint(lowX, highX)
            num2X = random.randint(lowX, highX)
            
            # 1 second to mentally prepare!
            print()
            sleep(1)

            # The question.. You've got 15 seconds!!
            product = num1X * num2X

            # Timer start
            start_time = time()
            # Your answer to the question..
            response = input(f'{num1X} * {num2X} = ')
            # Timer end
            elapsed_time = time() - start_time

            # Quit if no answer is given or player has run out of lives
            if not response or lives == 0:
                print('Game Over')
                break

            # Let's judge your answer
            try:
                answer = int(response)

                # Correct!
                if answer == product:
                    print(f'Well Done! Time elapsed: {elapsed_time:.2f}s')

                    # Less than 2 seconds is blazing.. Extra XP for being quick!
                    if elapsed_time < 2:
                        print('Speedy!')
                        placeholder_xp = placeholder_xp + 2
                        total_xp = total_xp + 2
                        print('Your XP is', total_xp)

                    # Regular XP for an on-time answer..
                    else:
                        placeholder_xp = placeholder_xp + 1
                        total_xp = total_xp + 1
                        print('Your XP is', total_xp)

                    # Too slow!
                    if elapsed_time > 15:
                        print('Too Slow!')
                        lives = lives - 1
                        print(f'You have {lives} lives left.')

                # Beep: Wrong!!
                else:
                    print("Incorrect")
                    lives = lives - 1
                    print(f'You have {lives} lives left.')
                    if lives == 0:
                        print('Game Over')

            # Not even a number :/ get wrecked..
            except ValueError:
                print('Try a number next time..')
                lives = lives - 1
                print(f'You have {lives} lives left.')
            

            # Level Up!!
            while placeholder_xp >= lvlNext:
                level += 1
                print(f'You are now Level {level}!')
                placeholder_xp = placeholder_xp - lvlNext
                lvlNext = round(lvlNext * 1.5)

                # Things get harder now..
                lowX = round(lowX + 1)
                highX = round(highX + 2)

        # Congratulations! You got a high score!
        newscore = update_leaderboard(player_name, total_xp)
        if is_top_ten(newscore, player_name, total_xp):
            while True:
                print('Congratulations! You got a high score!')
                print()
                sleep(1)
                display_leaderboard()
                print()
                go_back = input("Press any key to continue: ")
                if go_back == 'x':
                    break
                else:
                    break

    elif mode == 'l':
        while True:
            print()
            display_leaderboard()
            print()
            go_back = input("Press any key to continue: ")
            if go_back == 'x':
                break
            else:
                break


    # Exit main menu
    elif mode == 'x':
        # EXIT
        exit()

    # Something went terribly wrong
    else:
        print("Option not available.")
    
    