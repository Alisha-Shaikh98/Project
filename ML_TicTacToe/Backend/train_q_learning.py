import random
import pickle
from collections import defaultdict
from tqdm import trange

def board_to_state(board):
    return ','.join(map(str,board))

def available_actions(board):
    return [i for i, v in enumerate(board) if v==0]

def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),(0,3,6), (1,4,7), (2,5,8),(0,4,8), (2,4,6)]
    
    for a,b,c in wins:
        if board[a] !=0 and board[a] == board[b] and board[b] == board[c]:
            return board[a] #-1 or 1
    if 0 not in board:
            return 0 
    return None
    
class QLearner:
    def __init__(self,alpha=0.3, gamma=0.9, epsilon=1.0, min_epsilon=0.05, decay=0.99995):
        self.Q = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay

        
    def get_Qs(self, state):
        return self.Q[state]
    
    def choose_action(self, board):
        state = board_to_state(board)
        actions = available_actions(board)
        if not actions:
            return None
        
        #epsilon-greedy strategy
        if random.random() < self.epsilon:
            return random.choice(actions)

        qvals = self.Q[state]
        best = None
        best_val = -9e9
        for a in actions:
            val = qvals.get(a,0.0)
            if val> best_val:
                best_val = val
                best = [a]
            elif val == best_val:
                best.append(a)
        return random.choice(best)
    
    def learn(self, s,a,r,s_next, done):
        q_sa = self.Q[s].get(a,0.0)
        max_next = 0.0
        if not done:
            next_qs = self.Q[s_next]
            max_next = max(next_qs.values()) if next_qs else 0.0

            self.Q[s][a] = q_sa + self.alpha * (r + self.gamma * max_next - q_sa)

    def decay_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.decay
            if self.epsilon < self.min_epsilon:
                self.alpha = self.min_epsilon

def play_episode(agent, verbose = False):
    board = [0]*9
    current_player = 1
    history = []
    done = False

    while True:
        state = board_to_state(board)
        actions = available_actions(board)
        if not actions:
            result = 0
            break

        action = agent.choose_action(board)
        if action is None:
            result = 0 
            break 

        board[action] = current_player
        history.append((state,action, current_player))
        
        winner = check_winner(board)
        if winner is not None:
            result = winner
            break

        current_player *= -1 
    
    for i in range(len(history)-1,-1,-1):
        s,a,player = history[i]

        if result == 0:
            r = 0.5
        elif result == player:
            r = 1.0
        else:
            r = -1.0
        
        s_list = list(map(int, s.split(',')))
        s_list[a] = player
        s_next = ','.join(map(str, s_list))
        done_flag = (i== len(history)-1)
        agent.learn(s,a,r,s_next, done_flag)

    agent.decay_epsilon()
    return result

def train(episodes = 50000, show_progress = True):
    agent = QLearner(alpha=0.3, gamma = 0.9, epsilon=1.0, min_epsilon=0.05,decay = 0.999995)
    wins = {1:0,-1:0,0:0}
    rng = trange(episodes) if show_progress else range(episodes)
    for _ in rng:
        res = play_episode(agent)
        wins[res] = wins.get(res,0) + 1
        if show_progress and rng.total % 1000 == 0:
            pass

    return agent

if __name__ == "__main__":
    EPISODES = 50000
    print("Training Q-learner for ",EPISODES, "episodes...")
    agent = train(EPISODES, show_progress=True)

    q_table = dict(agent.Q)
    with open("q_table.pkl","wb") as f:
        pickle.dump(q_table, f)
    print("training finished, Q-table saved to q_table.pkl")
    print("Final epsilon: ",agent.epsilon)
