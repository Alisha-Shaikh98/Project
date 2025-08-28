from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import pickle
import os

app = Flask(__name__)
CORS(app)

Q_TABLE_PATH = "q_table.pkl"
q_table = {}

# --- Utilities ---
def board_to_state(board):
    return ','.join(map(str, board))

def available_actions(board):
    return [i for i, v in enumerate(board) if v == 0]

def check_winner(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in wins:
        if board[a] != 0 and board[a] == board[b] and board[b] == board[c]:
            return board[a]  # 1 or -1
    if 0 not in board:
        return 0  # draw
    return None

# --- Safe Q-table loading ---
if os.path.exists(Q_TABLE_PATH) and os.path.getsize(Q_TABLE_PATH) > 0:
    try:
        with open(Q_TABLE_PATH, "rb") as f:
            q_table = pickle.load(f)
        print("Loaded Q-table with", len(q_table), "states.")
    except Exception as e:
        print(f"Error loading Q-table: {e}. Starting with empty Q-table.")
        q_table = {}
else:
    print("Q-table file not found or empty. Starting with fallback mode.")
    q_table = {}

# --- Bot move logic ---
def q_move(board):
    state = board_to_state(board)
    actions = available_actions(board)
    if not actions:
        return None

    if state in q_table:
        actions_q = q_table[state]
        best = None
        best_val = -9e9
        for a in actions:
            val = actions_q.get(a, 0.0)
            if val > best_val:
                best_val = val
                best = [a]
            elif val == best_val:
                best.append(a)
        if best:
            return random.choice(best)

    # Fallback: try win/block
    for player in (-1, 1):
        for a in actions:
            newb = board.copy()
            newb[a] = player
            if check_winner(newb) == player:
                return a

    if 4 in actions:
        return 4
    corners = [i for i in [0, 2, 6, 8] if i in actions]
    if corners:
        return random.choice(corners)

    return random.choice(actions)

# --- Routes ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "TicTacToe Backend is Running"}), 200

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data.get("board", [])
    if len(board) != 9:
        return jsonify({"error": "Board must have 9 positions"}), 400

    move_idx = q_move(board)
    return jsonify({"move": move_idx})

if __name__ == "__main__":
    app.run(debug=True)
