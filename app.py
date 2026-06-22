import streamlit as st
import random
import time

# =========================
# TIC TAC TOE GAME CLASS
# =========================
class TicTacToe:

    def __init__(self):
        self.board = [""] * 9

    def make_move(self, position, player):

        if self.board[position] == "":
            self.board[position] = player
            return True

        return False

    def check_winner(self):

        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in winning_combinations:

            a, b, c = combo

            if (
                self.board[a] != ""
                and self.board[a] == self.board[b]
                and self.board[b] == self.board[c]
            ):
                return self.board[a]

        return None

    def is_draw(self):
        return "" not in self.board and self.check_winner() is None


# =========================
# AI PLAYER CLASS
# =========================
class AIPlayer:

    def check_winner(self, board):

        wins = [
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6],
            [1,4,7],
            [2,5,8],
            [0,4,8],
            [2,4,6]
        ]

        for a,b,c in wins:

            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a]

        if "" not in board:
            return "Draw"

        return None

    def minimax(self, board, is_maximizing):

        result = self.check_winner(board)

        if result == "⭕":
            return 1

        if result == "❌":
            return -1

        if result == "Draw":
            return 0

        if is_maximizing:

            best_score = -100

            for i in range(9):

                if board[i] == "":
                    board[i] = "⭕"

                    score = self.minimax(board, False)

                    board[i] = ""

                    best_score = max(score, best_score)

            return best_score

        else:

            best_score = 100

            for i in range(9):

                if board[i] == "":
                    board[i] = "❌"

                    score = self.minimax(board, True)

                    board[i] = ""

                    best_score = min(score, best_score)

            return best_score

    def best_move(self, board):

        best_score = -100
        move = None

        for i in range(9):

            if board[i] == "":

                board[i] = "⭕"

                score = self.minimax(board, False)

                board[i] = ""

                if score > best_score:
                    best_score = score
                    move = i

        return move


# =========================
# SESSION STATE
# =========================
if "game" not in st.session_state:
    st.session_state.game = TicTacToe()

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draws" not in st.session_state:
    st.session_state.draws = 0


game = st.session_state.game
ai = AIPlayer()

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

h1 {
    text-align: center;
    color: #38bdf8;
}

.stButton > button {
    width: 100%;
    height: 90px;
    font-size: 35px;
    font-weight: bold;
    border-radius: 15px;
    border: 2px solid #38bdf8;
    background-color: #1e293b;
    color: white;
}

.stButton > button:hover {
    background-color: #38bdf8;
    color: white;
}

.score-card {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# UI
# =========================
st.markdown(
    "<h1>🤖 AI Tic-Tac-Toe Pro</h1>",
    unsafe_allow_html=True
)

st.write("### You = ❌")
st.write("### AI = ⭕")

difficulty = st.sidebar.selectbox(
    "🎯 Difficulty",
    ["Easy", "Hard"]
)

# =========================
# SCOREBOARD
# =========================
st.sidebar.markdown("## 🏆 Scoreboard")

st.sidebar.metric(
    "👤 Player",
    st.session_state.player_score
)

st.sidebar.metric(
    "🤖 AI",
    st.session_state.ai_score
)

st.sidebar.metric(
    "🤝 Draws",
    st.session_state.draws
)
winner = game.check_winner()

# =========================
# RESULT
# =========================
if winner == "X":
    st.balloons()
    st.success("🎉 Congratulations! You Win!")

elif winner == "O":
    st.error("🤖 AI Wins!")

elif game.is_draw():
    st.warning("🤝 Draw Match")


# =========================
# BOARD
# =========================
for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        idx = row * 3 + col

        with cols[col]:

            if st.button(
                 "❌" if game.board[idx] == "❌"
                else "⭕" if game.board[idx] == "⭕"
                else " ",
                key=idx
            ):

                try:

                    if winner or game.is_draw():
                        st.stop()

                    if game.make_move(idx, "❌"):

                        if (
                            game.check_winner() is None
                            and not game.is_draw()
                        ):

                            if difficulty == "Easy":

                                available = [
                                    i for i in range(9)
                                    if game.board[i] == ""
                                ]

                                ai_move = random.choice(
                                    available
                                )

                            else:

                                with st.spinner(
                                    "🤖 AI is thinking..."
                                ):
                                    time.sleep(1)
                                    ai_move = ai.best_move(
                                        game.board
                                    )

                            if ai_move is not None:
                                game.make_move(
                                    ai_move,
                                    "⭕"
                                )

                        st.rerun()

                except Exception as e:
                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================
# UPDATE SCORES
# =========================
if winner == "❌":

    if "counted" not in st.session_state:
        st.session_state.player_score += 1
        st.session_state.counted = True

elif winner == "⭕":

    if "counted" not in st.session_state:
        st.session_state.ai_score += 1
        st.session_state.counted = True

elif game.is_draw():

    if "counted" not in st.session_state:
        st.session_state.draws += 1
        st.session_state.counted = True


# =========================
# RESTART BUTTON
# =========================
if st.button("🔄 New Game"):

    st.session_state.game = TicTacToe()

    if "counted" in st.session_state:
        del st.session_state.counted

    st.rerun()


# =========================
# RESET SCORES
# =========================
if st.sidebar.button("Reset Scores"):

    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draws = 0

    st.session_state.game = TicTacToe()

    if "counted" in st.session_state:
        del st.session_state.counted

    st.rerun()
st.markdown("---")

st.markdown(
"""
<center>
Made with ❤️ using Python, OOP, AI & Streamlit
</center>
""",
unsafe_allow_html=True
)
