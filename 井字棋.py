class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def print_board(self):
        print("-------------")
        for i in range(3):
            print("|", end=" ")
            for j in range(3):
                print(self.board[i*3+j], "|", end=" ")
            print("\n-------------")

    def place_mark(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            print("该位置已被占用，请重新选择。")

    def check_win(self):
        for player in ['X', 'O']:
            # 检查行
            for i in range(0, 9, 3):
                if self.board[i] == self.board[i+1] == self.board[i+2] == player:
                    return True

            # 检查列
            for i in range(3):
                if self.board[i] == self.board[i+3] == self.board[i+6] == player:
                    return True

            # 检查对角线
            if self.board[0] == self.board[4] == self.board[8] == player or \
               self.board[2] == self.board[4] == self.board[6] == player:
                   return True
        return False
    def play_game(self):
        self.print_board()
        while not self.check_win() and ' ' in self.board:
            position = int(input(f"轮到玩家{self.current_player}，请输入您的位置（1-9）："))
            self.place_mark(position-1)
            self.print_board()

        if self.check_win():
            print(f"恭喜玩家{self.current_player}，您输了！")
        elif ' ' not in self.board:
            print("平局！")

game = TicTacToe()
game.play_game()

game = TicTacToe()
game.play_game()