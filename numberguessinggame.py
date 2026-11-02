import random
import mysql.connector
from datetime import date

# ==================== DATABASE SETUP ====================

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",
        database="game_db"
    )
    return conn


def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS game_db")
    cursor.execute("USE game_db")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(30),
        game_type VARCHAR(20),
        result VARCHAR(10),
        attempts INT,
        date VARCHAR(12)
    )
    """)
    conn.commit()
    conn.close()


def save_score(username, game_type, result, attempts):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO scores (username, game_type, result, attempts,
    date)
    VALUES (%s, %s, %s, %s, %s)
    """, (username, game_type, result, attempts, str(date.today())))
    conn.commit()
    conn.close()


def show_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*50)
    print(" LEADERBOARD - NUMBER GUESSING (Fewest Attempts)")
    print("="*50)
    cursor.execute("""
    SELECT username, attempts, date FROM scores
    WHERE game_type = 'Number' AND result = 'Win'
    ORDER BY attempts ASC LIMIT 5
    """)
    rows = cursor.fetchall()
    if rows:
        for i, row in enumerate(rows, 1):
            print(f"{i}. {row[0]} - {row[1]} attempts ({row[2]})")
    else:
        print("No scores yet!")

    print()
    conn.close()


# ==================== NUMBER GUESSING GAME ====================

def number_guessing_game(username):
    restart = True
    while restart:
        secret_number = random.randint(1, 3000)
        attempts = 0
        guessed = False

        print("Welcome to the Number Guessing Game!")
        print("I have selected a number between 1 and 3000.")
        print("Try to guess it!\n")

        while not guessed:
            try:
                guess = int(input("Enter your guess: "))
                attempts = attempts + 1

                if guess < 1 or guess > 3000:
                    print("Please enter a number between 1 and "
                          "3000!\n")
                    continue

                difference = abs(guess - secret_number)

                if guess == secret_number:
                    guessed = True
                    print("Congratulations! You guessed it!")
                    print("The number was", secret_number)
                    print("You took", attempts, "attempts.\n")
                    save_score(username, "Number", "Win", attempts)
                    dec = input("Do you wish to continue? Y/N: ")
                    if dec in "Yy":
                        guessed = False
                    else:
                        restart = False
                else:
                    direction = "Higher!" if guess < secret_number else "Lower!"

                    if difference <= 5:
                        temperature = "BURNING HOT!"
                    elif difference <= 20:
                        temperature = "VERY HOT!"
                    elif difference <= 200:
                        temperature = "HOT!"
                    elif difference <= 500:
                        temperature = "Neutral"
                    elif difference <= 1200:
                        temperature = "Cold"
                    else:
                        temperature = "VERY COLD"

                    print(direction, temperature)
                    print("Attempts:", attempts, "\n")

            except ValueError:
                print("Invalid input! Please enter a valid "
                      "number.\n")


# ==================== MAIN ====================

def main():
    init_db()

    username = input("Enter your username: ").strip()
    if not username:
        username = "Anonymous"

    while True:
        print("\n" + "="*40)
        print(f"Welcome, {username}!")
        print("GAME SELECTION")
        print("="*40)
        print("1. Number Guessing Game")
        print("2. View Leaderboard")
        print("3. Exit")
        print("="*40)

        try:
            choice = input("Which game do you want to play? "
                           "(1/2/3): ")
            if choice == "1":
                number_guessing_game(username)
            elif choice == "2":
                show_leaderboard()
            elif choice == "3":
                show_leaderboard()
                print("Thanks for playing! Goodbye")
                break
            else:
                print("Invalid choice! Please enter 1, 2 or 3.\n")

        except ValueError:
            print("Invalid input!\n")


main()