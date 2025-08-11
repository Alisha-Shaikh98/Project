from flask import Flask,request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

#Simple bot logic
def get_bot_move(board):
    #find all empty position on board and store their index
    empty_positions = [i for i, cell in enumerate(board)if cell==0]
    if not empty_positions:
        return None
    return random.choice(empty_positions) #Pick randomly

@app.route("/move",methods=["POST"])
def move():
    data = request.get_json()
    board = data.get("board",[])
    
    #Validate board length
    if len(board) !=9:
        return jsonify({"error": "Board must have 9 positions"}), 400
    bot_move = get_bot_move(board)
    return jsonify({"move": bot_move})

if __name__ =="__main__":
    app.run(debug=True)