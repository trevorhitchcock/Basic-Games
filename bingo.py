import random

# initialize board_size for the game
BOARD_SIZE = 5

class Board:
    def __init__(self, card, index_called, player_number):
        self.card = card
        self.index_called = index_called
        self.player_number = player_number
    
    # prints board
    def __str__(self):
        print_string = "\nBoard "+str(self.player_number)+":"
        for i in range(len(self.card)):
            print_string += "\n"
            for j in range(len(self.card[i])):
                # print [i,j] to organize by columns instead of rows
                if(self.index_called[j][i]) == True:
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
    
    def populate_board(self):
        global BOARD_SIZE
        
        # bounds for random number generation
        low_bound = 1
        high_bound = 15
        for i in range(len(self.card)):
            # Generate a list of unique numbers for this row
            row_numbers = set()
            while len(row_numbers) < BOARD_SIZE:
                num = random.randint(low_bound, high_bound)
                row_numbers.add(num)
            row_numbers = list(row_numbers)
            random.shuffle(row_numbers)
            # Assign the shuffled numbers to the row
            self.card[i] = row_numbers
            # Increase bounds for the next row
            low_bound += 15
            high_bound += 15

        # Set middle space to 0 (represents free space)
        middle_space = len(self.card) // 2
        self.card[middle_space][middle_space] = 0
        
        return self.card
    
    def update_index_called_board(self, called_number):
        # check if called number in card
        for i in range(len(self.card)):
            for j in range(len(self.card[i])):
                # if number found, set index_called to true
                if self.card[i][j] == called_number:
                    self.index_called[i][j] = True
    
    def check_win(self):
        # check columns
        for i in range(len(self.index_called)):
            if False not in self.index_called[i]:
                # if False not in any index, list must be full of True, board won
                return True
        
        # check rows
        for i in range(len(self.index_called)):
            streak = 0
            for j in range(len(self.index_called[i])):
                if(self.index_called[i][j]) == True:
                    streak +=1
                if streak == 5:
                    # 5 True's found in a row, board won
                    return True
            
def create_boards(players_count):
    
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
        
        # player_number is i+1 to not have player count start at 0
        cur_board = Board(card, index_called, i+1)
        cur_board.populate_board()
        
        #stores boards created
        boards_list.append(cur_board)
        print(cur_board)
    print("\nReady to play? Press enter!")
    
    # order in which numbers will be called
    called_numbers = list(range(1,76))
    random.shuffle(called_numbers)
    
    # for each number called
    for called_number in called_numbers:
        input()
        print("\n\nNumber called:",called_number)
        for board in boards_list:
            # check if called number is in each board
            board.update_index_called_board(called_number)
            print(board)
            if board.check_win():
                break

def main():
    print("Welcome to bingo! How many boards would you like to play?")
    #players = int(input())
    # OVERRIDE LATER
    create_boards(2)
    

if __name__ == "__main__":
    main()