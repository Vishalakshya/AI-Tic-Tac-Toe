import tkinter as tk

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("420x520")
        self.root.configure(bg="#1E1E2F")
        self.root.resizable(False, False)

        self.current_player = "X"
        self.buttons = [[None]*3 for _ in range(3)]
        self.board_state = [[""]*3 for _ in range(3)]

        # Status label
        self.status_label = tk.Label(
            root,
            text="Player X's Turn",
            font=("Segoe UI", 20, "bold"),
            fg="#E0E0E0",
            bg="#1E1E2F"
        )
        self.status_label.pack(pady=20)

        # Board frame (card style)
        self.board_frame = tk.Frame(
            root,
            bg="#2A2A3D",
            padx=15,
            pady=15
        )
        self.board_frame.pack()

        # Buttons
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Segoe UI", 32, "bold"),
                    width=3,
                    height=1,
                    bg="#3A3A55",
                    fg="white",
                    relief="flat",
                    activebackground="#5C5C85",
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                btn.grid(row=i, column=j, padx=8, pady=8)
                self.buttons[i][j] = btn

        # Reset button
        self.reset_button = tk.Button(
            root,
            text="RESET GAME",
            font=("Segoe UI", 14, "bold"),
            bg="#7C4DFF",
            fg="white",
            relief="flat",
            activebackground="#9575CD",
            padx=20,
            pady=8,
            command=self.reset_game
        )
        self.reset_button.pack(pady=20)

    def on_click(self, row, col):
        if self.current_player == "O":
            return

        if self.board_state[row][col] != "":
            return

        self.board_state[row][col] = "X"
        self.buttons[row][col].config(text="X", fg="#4FC3F7")

        if self.check_for_win():
            self.status_label.config(text="Player X Wins!")
            self.highlight_winning_line()
            self.disable_all_buttons()
        elif self.is_board_full():
            self.status_label.config(text="It's a Draw!")
        else:
            self.current_player = "O"
            self.status_label.config(text="AI is thinking...")
            self.root.after(500, self.ai_move)

    def ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board_state[i][j] == "":
                    self.board_state[i][j] = "O"
                    score = self.minimax(self.board_state, False)
                    self.board_state[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            r, c = best_move
            self.board_state[r][c] = "O"
            self.buttons[r][c].config(text="O", fg="#FF8A65")

        if self.check_for_win():
            self.status_label.config(text="AI Wins!")
            self.highlight_winning_line()
            self.disable_all_buttons()
        elif self.is_board_full():
            self.status_label.config(text="It's a Draw!")
        else:
            self.current_player = "X"
            self.status_label.config(text="Player X's Turn")

    def minimax(self, board, is_maximizing):
        if self.check_winner(board, "O"):
            return 1
        if self.check_winner(board, "X"):
            return -1
        if self.is_full(board):
            return 0

        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O"
                        best = max(best, self.minimax(board, False))
                        board[i][j] = ""
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "X"
                        best = min(best, self.minimax(board, True))
                        board[i][j] = ""
            return best

    def check_for_win(self):
        return self.check_winner(self.board_state, "X") or self.check_winner(self.board_state, "O")

    def check_winner(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)): return True
            if all(board[j][i] == player for j in range(3)): return True
        if all(board[i][i] == player for i in range(3)): return True
        if all(board[i][2-i] == player for i in range(3)): return True
        return False

    def highlight_winning_line(self):
        winner = "X" if self.check_winner(self.board_state, "X") else "O"
        for i in range(3):
            if all(self.board_state[i][j] == winner for j in range(3)):
                for j in range(3): self.buttons[i][j].config(bg="#66BB6A")
                return
            if all(self.board_state[j][i] == winner for j in range(3)):
                for j in range(3): self.buttons[j][i].config(bg="#66BB6A")
                return
        if all(self.board_state[i][i] == winner for i in range(3)):
            for i in range(3): self.buttons[i][i].config(bg="#66BB6A")
        if all(self.board_state[i][2-i] == winner for i in range(3)):
            for i in range(3): self.buttons[i][2-i].config(bg="#66BB6A")

    def is_board_full(self):
        return self.is_full(self.board_state)

    def is_full(self, board):
        return all(cell != "" for row in board for cell in row)

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#3A3A55", state="normal")
                self.board_state[i][j] = ""
        self.current_player = "X"
        self.status_label.config(text="Player X's Turn")


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
