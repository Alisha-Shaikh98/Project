from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import pickle
import os

app = Flask(__name__)
CORS(app)

Q_TABLE_PATH = "q_table.pkl"
q_table = {}

# --- Utilities (same representation as trainer) ---
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

# --- Load Q-table if available ---
if os.path.exists(Q_TABLE_PATH):
    with open(Q_TABLE_PATH, "rb") as f:
        q_table = pickle.load(f)
    # ensure keys are strings and actions map to floats
    # q_table format: {state_str: {action_index: value, ...}, ...}
    print("Loaded Q-table with", len(q_table), "states.")
else:
    print("Warning: q_table.pkl not found. Bot will use fallback heuristics/random moves.")

# --- Bot move using q-table with safe fallback ---
def q_move(board):
    state = board_to_state(board)
    actions = available_actions(board)
    if not actions:
        return None
    # If state in q_table, pick best action among available ones
    if state in q_table:
        actions_q = q_table[state]
        # pick best action among available; if unseen, fallback
        best = None
        best_val = -9e9
        for a in actions:
            val = actions_q.get(a, 0.0)
            if val > best_val:
                best_val = val
                best = [a]
            elif val == best_val:
                best.append(a)
        if best is not None:
            return random.choice(best)
    # else fallback heuristics (simple rule-based)
    # Try win, block, center, corners, sides
    # Check win opportunity for us (-1) and block human (1)
    # For simplicity, we use a helper to test moves
    for player in (-1, 1):  # first try to make winning move, then block
        for a in actions:
            newb = board.copy()
            newb[a] = player
            if check_winner(newb) == player:
                # If player == -1, it's our winning move; if 1, it's a blocking move
                return a
    # take center
    if 4 in actions:
        return 4
    # take a random corner
    corners = [i for i in [0,2,6,8] if i in actions]
    if corners:
        return random.choice(corners)
    # fallback random
    return random.choice(actions)

# Simple random move (in case nothing else)
def random_move(board):
    actions = available_actions(board)
    return random.choice(actions) if actions else None

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data.get("board", [])
    if len(board) != 9:
        return jsonify({"error": "Board must have 9 positions"}), 400

    # choose move from Q-table or fallback
    move_idx = q_move(board)
    return jsonify({"move": move_idx})

if __name__ == "__main__":
    app.run(debug=True)