import streamlit as st


class TicTacToe:
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"

    def make_move(self, position):
        if self.board[position] == "":
            self.board[position] = self.current_player
            return True
        return False

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in winning_combinations:
            a, b, c = combo

            if (
                self.board[a] != "" and
                self.board[a] == self.board[b] ==
                self.board[c]
            ):
                return self.board[a]

        return None

    def is_draw(self):
        return "" not in self.board


# Session State
if "game" not in st.session_state:
    st.session_state.game = TicTacToe()

game = st.session_state.game

st.title("🎮 Tic-Tac-Toe")

winner = game.check_winner()

if winner:
    st.success(f"Player {winner} Wins! 🏆")
elif game.is_draw():
    st.warning("Match Draw 🤝")
else:
    st.info(f"Current Player: {game.current_player}")

# Create Board
for row in range(3):
    cols = st.columns(3)

    for col in range(3):
        idx = row * 3 + col

        with cols[col]:
            if st.button(
                game.board[idx] if game.board[idx] else " ",
                key=idx
            ):
                try:
                    if not winner and not game.is_draw():
                        if game.make_move(idx):
                            game.switch_player()
                            st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# Restart Button
if st.button("Restart Game"):
    st.session_state.game = TicTacToe()
    st.rerun()