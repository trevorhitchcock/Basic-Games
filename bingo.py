import random

# initialize board_size for the game
BOARD_SIZE: int = 5

class Board:
    def __init__(self, card: list(list()), index_called: list(list()), name: str):
        self.card = card
        self.index_called = index_called
        self.name = name
    
    # prints board
    def __str__(self):
        print_string = "\n"+str(self.name)+"'s Board:\nB   I   N   G   O"
        for i in range(len(self.card)):
            print_string += "\n"
            for j in range(len(self.card[i])):
                # print [i,j] to organize by columns instead of rows
                if(self.index_called[j][i]) == True:
                    # if index has been called, print unicode green space instead of number
                    print_string += "\U0001F7E9 "
                # add three spaces if less than 10, else add two. for printing purposes
                elif(self.card[j][i]<10):
                    print_string += str(self.card[j][i])+ "   "
                else:
                    print_string += str(self.card[j][i])+ "  "
                    
        # extra code to print index_called board for testing
        """
        print_string += "\nIndex called board:"
        for i in range(len(self.index_called)):
            print_string += "\n"
            for j in range(len(self.index_called[i])):
                # also prints in the form [i][j] to keep consistent
                print_string += str(self.index_called[j][i]) + " "
                """
        return print_string
    
    def populate_board(self) -> list:
        """
        Populates the board with random unique numbers for each index.

        :return: The populated board.
        """
        global BOARD_SIZE
        
        # bounds for random number generation
        low_bound = 1
        high_bound = 15
        for i in range(len(self.card)):
            # generate a list of unique numbers for this row
            # set to avoid duplicates
            row_numbers = set()
            while len(row_numbers) < BOARD_SIZE:
                num = random.randint(low_bound, high_bound)
                row_numbers.add(num)
            row_numbers = list(row_numbers)
            # set is sorted so must be shuffled after being placed in a list
            random.shuffle(row_numbers)
            # assigns the shuffled numbers to the row
            self.card[i] = row_numbers
            # increases bounds for the next row
            low_bound += 15
            high_bound += 15

        # sets middle space to 0 (represents free space)
        middle_space = len(self.card) // 2
        self.card[middle_space][middle_space] = 0
        
        return self.card
    
    def update_index_called_board(self, called_number: int) -> None:
        """
        Updates the index_called board to mark the called number as True if it exists on the board.

        :param called_number: The number that was called.
        """
        # check if called number in card
        for i in range(len(self.card)):
            for j in range(len(self.card[i])):
                # if number found, set index_called to true
                if self.card[i][j] == called_number:
                    self.index_called[i][j] = True
    
    def check_win(self) -> str:
        """
        Checks if the board has a winning combination (any column, row, or diagonal fully marked).

        :return: The name of the player if a win is detected, otherwise None.
        """
        global BOARD_SIZE
        
        # check columns
        for col in range(BOARD_SIZE):
            if all(self.index_called[col]):
                return self.name
        
        # check rows
        for row in range(BOARD_SIZE):
            if all(self.index_called[col][row] for col in range(BOARD_SIZE)):
                return self.name
                
        # check left-to-right diagonal
        if all(self.index_called[i][i] for i in range(BOARD_SIZE)):
            return self.name

        # check right-to-left diagonal
        if all(self.index_called[i][BOARD_SIZE - i - 1] for i in range(BOARD_SIZE)):
            return self.name

        return None
            
def create_boards(players_count: int) -> list:
    """
    Creates and returns a list of boards for the specified number of players.

    :param players_count: The number of players.
    :return: A list of Board objects.
    """
    boards_list = []
    # create a board for each player
    global BOARD_SIZE
    for i in range(players_count):
        # creates BOARD_SIZE x BOARD_SIZE matrix of 0s to initialize board
        card = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        
        # creates BOARD_SIZE x BOARD_SIZE matrix of False to store which indexes have been called
        index_called = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        middle_space = BOARD_SIZE // 2
        index_called[middle_space][middle_space] = True
        
        # input player names
        player_name = input("\nEnter the name for player "+str(i+1)+": ")
        # initalizes Board object
        cur_board = Board(card, index_called, player_name)
        cur_board.populate_board()
        
        #stores boards created
        boards_list.append(cur_board)
        print(cur_board)
    return boards_list

def call_numbers(boards_list: list) -> str:
    """
    Calls numbers randomly and updates the boards accordingly until a player wins.

    :param boards_list: The list of Board objects.
    :return: The name of the winning player.
    """
    print("\nReady to play? Press enter to call the next number!")
    
    # order in which numbers will be called
    called_numbers = list(range(1,76))
    random.shuffle(called_numbers)
    
    # for each number called
    for called_number in called_numbers:
        # input so users can play one step at a time
        input()
        
        # handles printing letter with number, uses string concatination
        number_print: str = "\n\nNumber called: "
        if(called_number <= 15):
            number_print += "B "
        elif(called_number <= 30):
            number_print += "I "
        elif(called_number <= 45):
            number_print += "N "
        elif(called_number <= 60):
            number_print += "G "
        else:
            number_print += "O "
        number_print += str(called_number)
        print(number_print)
        
        for board in boards_list:
            # check if called number is in each board
            board.update_index_called_board(called_number)
            print(board)
            
            player_won = board.check_win()
            if player_won != None:
                return player_won

def main():
    """
    Main function to run the Bingo game. Initializes the game, creates boards, and starts calling numbers.
    """
    
    print("Welcome to Bingo in Python! How many boards would you like to play?")
    
    while(True):
        
        # so the user only enters an int > 1
        try:
            players = int(input())
            if players < 1:
                print("Please enter a valid number of players (1 or more).")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            continue
        
        # create boards with inputted number of players
        boards_list = create_boards(players)
        
        # starts calling numbers with created board
        player_won: str = call_numbers(boards_list)
        print(player_won+" has won! Congratulations "+player_won+"!\n")
        
        play_again = input("Would you like to play again? (Y/N): ")
        # validate input
        while(play_again != "Y")and(play_again != "N"):
            print("Please enter 'Y' or 'N'")
            play_again = input("Would you like to play again? (Y/N): ")
        
        # play again
        if(play_again == "Y"):
            print("\nLet's play again. How many boards would you like to play?")
        else:
            print("Exiting...")
            break
        
if __name__ == "__main__":
    main()