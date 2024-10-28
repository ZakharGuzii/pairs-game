import random
import string
import time
import os

def create_matrix(cards_number):
    rows = 1
    cols = cards_number
    for i in range(1, int(cards_number ** 0.5) + 1):
        if cards_number % i == 0:
            rows = i
            cols = cards_number // i
    matrix = [['X' for _ in range(cols)] for _ in range(rows)]
    return matrix

def create_dictionary_from_matrix(matrix):
    matrix_dict = {}
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            key = f"{chr(c + ord('A'))}{r + 1}"
            matrix_dict[key] = matrix[r][c]
    return matrix_dict

def replace_with_random_symbols(matrix_dict, difficult_level):
    if difficult_level == 1:
        symbols = string.digits
    elif difficult_level == 2:
        symbols = string.ascii_lowercase
    else:
        symbols = string.ascii_letters + string.digits + string.punctuation
    unique_symbols = random.sample(symbols, len(matrix_dict) // 2)
    symbols_to_use = unique_symbols * 2
    random.shuffle(symbols_to_use)
    for index, key in enumerate(matrix_dict.keys()):
        matrix_dict[key] = [symbols_to_use[index], "X"]

def print_formatted_matrix(matrix_dict, rows, cols):
    HEADER_COLOR = '\033[94m'
    ROW_NUMBER_COLOR = '\033[93m'
    RESET = '\033[0m'
    header = "  " + "  ".join(f"{HEADER_COLOR}{chr(i + ord('A'))}{RESET}" for i in range(cols))
    print(header)
    for r in range(1, rows + 1):
        row_values = []
        row_number = f"{ROW_NUMBER_COLOR}{r}{RESET}"
        for c in range(1, cols + 1):
            key = f"{chr(c + ord('A') - 1)}{r}"
            value = matrix_dict.get(key, ['X', 'X'])
            row_values.append(value[1])
        print(f"{row_number} {'  '.join(row_values)}")

def update_matrix(matrix_dict, rows, cols):
    print_formatted_matrix(matrix_dict, rows, cols)
    valid_keys = matrix_dict.keys()
    key1 = input("\nPlease enter coordinates of first card: ").strip().upper()
    while key1 not in valid_keys:
        print(f"Coordinates of the card: {key1} was not found. Please try again.")
        key1 = input("Please enter coordinates of first card: ").strip()
    key2 = input("Please enter coordinates of second card: ").strip()
    while key2 not in valid_keys:
        print(f"Coordinates of the card: {key2} was not found. Please try again.")
        key2 = input("Please enter coordinates of second card:  ").strip()
    while key1 == key2:
        print("You cannot select the same card twice. Please enter different coordinates.")
        key2 = input("Please enter coordinates of second card: ").strip()
        while key2 not in valid_keys:
            print(f"Coordinates of the card: {key2} was not found. Please try again.")
            key2 = input("Please enter coordinates of second card: ").strip()
    if key1 in matrix_dict:
        matrix_dict[key1][1] = matrix_dict[key1][0]
    if key2 in matrix_dict:
        matrix_dict[key2][1] = matrix_dict[key2][0]
    print_formatted_matrix(matrix_dict, rows, cols)
    return matrix_dict[key1][0] == matrix_dict[key2][0], key1, key2

print("The game has several difficulty levels. \n"
      "0 - if you want choose standart game and thinking about nothing\n"
      "1 - only numbers and maximum number of cards - 20. \n"
      "2 - only small letters, maximum number of cards - 48. \n"
      "3 - numbers, big and small letters and special characters, maximum number of cards - 184.")
while True:
    try:
        difficult_level = int(input("Choose from existing difficulty levels: "))
        if difficult_level  == 1 or difficult_level  == 2 or difficult_level  == 3 or difficult_level  == 0:
            break
        else:
            print("Incorrect input. Choose from existing difficulty levels.")
    except ValueError:
        print("Enter the suggested difficulty for the game.")
if difficult_level==0:
    cards_number=16
    game_duration = 180
    cards_showing = 5
    correct_cards_showing = 'yes'
else:
    while True:
        try:
            cards_number = int(input("Enter the number of cards(not unique) you want to play: "))
            if cards_number % 2 == 0 and cards_number > 2:
                if difficult_level == 1 and cards_number<=20:
                    break
                elif difficult_level == 2 and cards_number<=48:
                    break
                elif difficult_level == 3 and cards_number<=184:
                    break
            else:
                print("Enter the even number of cards that corresponds to the complexity of the game.")
        except ValueError:
            print("Enter the even number of cards that corresponds to the complexity of the game.")
    while True:
        try:
            game_duration = int(input("Enter the game duration in seconds: "))
            if game_duration>=0:
                break
            else:
                print("Unfortunately, you can't turn back the clock. Enter a positive number.")
        except ValueError:
            print("Enter a positive number.")
    while True:
        try:
            cards_showing = int(input("How many seconds you want the cards to be visible: "))
            if game_duration>=cards_showing and cards_showing>=0:
                break
            else:
                print("Unfortunately, you can't turn back the clock. Enter a positive number. It cannot exceed the total amount of time")
        except ValueError:
            print("Incorrect input.")
    while True:
        try:
            correct_cards_showing = input("Do you want the correct cards to be shown at all times? (Yes/No): ")
            if correct_cards_showing.lower().strip() == 'yes' or correct_cards_showing.lower().strip()=='no':
                break
            else:
                print("Enter the suggested words. (Yes/No)")
        except ValueError:
            print("Incorrect input. Enter the suggested words. (Yes/No)")

start_matrix = create_matrix(cards_number)
start_dict = create_dictionary_from_matrix(start_matrix)
replace_with_random_symbols(start_dict, difficult_level)
rows_for_printing = len(start_matrix)
cols_for_printing  = len(start_matrix[0])

matches = 0
attempts = 0
total_pairs = len(start_dict) // 2
open_identical_cards = set()
win = False
game_started = False

while matches < total_pairs:
    if not game_started:
        start_time = time.time()
        game_started = True
    is_match, key1, key2 = update_matrix(start_dict, rows_for_printing, cols_for_printing)
    if game_started:
        elapsed_time = time.time() - start_time
        if elapsed_time > game_duration:
            print("Time is up! You've exceeded your allotted time.")
            time.sleep(10)
            win = False
            break
    if key1 in open_identical_cards or key2 in open_identical_cards:
        print('You have already guessed one of these cards. Please choose different coordinates.')
        if key1 in open_identical_cards:
            start_dict[key2][1] = 'X'
        else:
            start_dict[key1][1] = 'X'
        time.sleep(cards_showing)
        os.system('cls' if os.name == 'nt' else 'clear')
        continue
    if is_match:
        print('Congratulations, you guessed a pair')
        open_identical_cards.add(key1)
        open_identical_cards.add(key2)
        matches += 1
        if correct_cards_showing.lower().strip() == 'no':
            time.sleep(cards_showing)
            start_dict[key1][1] = 'X'
            start_dict[key2][1] = 'X'
            os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print('Unfortunately, the numbers do not match')
        time.sleep(cards_showing)
        os.system('cls' if os.name == 'nt' else 'clear')
        start_dict[key1][1] = 'X'
        start_dict[key2][1] = 'X'
    attempts += 1
    if matches == total_pairs:
        win = True
        break

if win:
    print(f"Congratulations! You've found all the matches! It took you only {attempts} attempts to guess all the cards.")
    time.sleep(10)
else:
    print("Unfortunately, you couldn't win. Next time will definitely be better!")
    time.sleep(10)