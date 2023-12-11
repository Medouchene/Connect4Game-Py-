from tkinter import *
class Connect4Game(object):
    def __init__(self):
        self.board = list()
        for _ in range(6):
            self.board.append([0] * 7)

    def display(self):
        for row in self.board:
            for case in row:
                if case == 1:
                    symbol = 'X'
                elif case == 2:
                    symbol = 'O'
                else:
                    symbol = ' '
                print(f'|{symbol}', end=' ')
            print('|')
        print('=============================')
        for i in range(len(self.board[1])):
            print(f' {i + 1}', end=' ')
        print(' ')

    def pieces_in_column(self, column_num):
        count = 0
        if column_num > 8 or column_num < 0:
            return False
        else:
            for row in range(6):
                if self.board[row][column_num - 1] != 0:
                    count += 1
            return count

    def stack_piece(self, column_num, color):
        if column_num < 0 or column_num > 8:
            return False
        else:
            num_pieces = self.pieces_in_column(column_num)
            self.board[5 - num_pieces][column_num - 1] = color

    def pieces_in_direction(self, row, col, delta_row, delta_col):
        count = 0
        piece = self.board[row][col]
        while (
            row + delta_row >= 0
            and row + delta_row < len(self.board)
            and col + delta_col >= 0
            and col + delta_col < len(self.board[row])
            and self.board[row + delta_row][col + delta_col] == piece
        ):
            count += 1
            row += delta_row
            col += delta_col
        return count

    def test_rows(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != 0:
                    if self.pieces_in_direction(row, col, 0, 1) >= 3:
                        return True
                    elif self.pieces_in_direction(row, col, 0, -1) >= 3:
                        return True

    def test_columns(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != 0:
                    if self.pieces_in_direction(row, col, 1, 0) >= 3:
                        return True
                    elif self.pieces_in_direction(row, col, -1, 0) >= 3:
                        return True

    def test_diagonals(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != 0:
                    if self.pieces_in_direction(row, col, 1, 1) >= 3:
                        return True
                    elif self.pieces_in_direction(row, col, -1, 1) >= 3:
                        return True
                    elif self.pieces_in_direction(row, col, -1, -1) >= 3:
                        return True
                    elif self.pieces_in_direction(row, col, 1, -1) >= 3:
                        return True

    def test_all(self):
        if self.test_columns():
            return True
        elif self.test_rows():
            return True
        elif self.test_diagonals():
            return True
        return False

    def play_game(self):
        new_game = input("New game? ")
        while new_game.lower() == "yes":
            start_player = int(input("Who starts (1 or 2): "))
            if start_player == 2:
                start_player = 0

            for turn in range(
                start_player, start_player + (len(self.board[0]) * len(self.board))
            ):
                if turn % 2 == 0:
                    player = 2
                else:
                    player = 1

                column = int(input("Choose your column:"))
                while (
                    column <= 0
                    or column > 7
                    and column < 666
                    or self.pieces_in_column(column) == 6
                ):
                    column = int(
                        input("Invalid column, choose a column between 1 and 7:")
                    )

                print(player)

                if column == 666:
                    break

                self.stack_piece(column, player)
                self.display()
                turn += 1

                if self.test_all():
                    print("The winning player is:", player)
                    new_game = input("New game? ")
                    for i, x in enumerate(self.board):
                        for j, a in enumerate(x):
                            if 1 or 2 in a:
                                self.board[i][j] = 0
                    break
                break
        return None






class Application():
    def __init__(self):
        self.id = -1
        self.num_rows = 6
        self.num_columns = 7
        self.game = Connect4Game()
        self.current_player = 1
        self.window = Tk()
        self.window.title('Connect 4 Game')
        self.colors = ['red', 'blue']
        start_button = Button(self.window, text="New Game", command=self.new_game)
        quit_button = Button(self.window, text="Quit", command=self.window.destroy)
        start_button.pack()
        quit_button.pack()
        self.canvas = Canvas(self.window, width=400, height=430, bg='white')
        self.canvas.pack(side=TOP, padx=5, pady=5)
        self.canvas.create_rectangle(20, 400, 100, 420, fill='grey')
        self.canvas.create_text(50, 410, text='Player ')

        self.window.mainloop()

    def draw_board(self):
        for i in range(7):
            for j in range(6):
                x1 = i * 57 + 4
                y1 = 60 * j + 25
                x2 = 50 + 57 * i + 4
                y2 = 50 + 60 * j + 25
                self.canvas.create_oval(x1, y1, x2, y2, fill='white')
        self.canvas.pack(side=TOP, padx=5, pady=5)

    def new_game(self):
        self.draw_board()
        self.canvas.bind('<Button-1>', self.click)
        if self.id != -1:
            self.canvas.delete(self.id)
        self.game = Connect4Game()

    def click(self, event):
        x = event.x
        y = event.y
        column = 0
        radius = 25

        if 0 < x < 57:
            column = 1
        elif 57 <= x < 114:
            column = 2
        elif 114 <= x < 171:
            column = 3
        elif 171 <= x < 228:
            column = 4
        elif 228 <= x < 285:
            column = 5
        elif 285 <= x < 342:
            column = 6
        elif 342 <= x < 400:
            column = 7

        row = self.game.pieces_in_column(column)
        if row < 6:
            self.game.stack_piece(column, self.current_player)

            self.canvas.create_oval(75, 403, 90, 417, fill=self.colors[1 - (self.current_player - 1)])

            if self.game.test_all():
                self.id = self.canvas.create_text(
                    200, 200, text=f'Player {self.current_player} wins', font=('Helvetica 20 bold')
                )
                self.canvas.unbind('<Button-1>')

            self.canvas.create_oval(
                (column - 1) * 57 + 4, 60 * (5 - row) + 25, 50 + 57 * (column - 1) + 4,
                50 + 60 * (5 - row) + 25, fill=self.colors[self.current_player - 1]
            )

            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1


app = Application()
app.draw_board()














