# game_logic.py
from game_state import GameState
from constants import *
import random

def evaluate_position(state, player):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    weights = {
        5: 100000,    # Win
        4: {
            'open': 50000,    # Open four (winning threat)
            'closed': 10000   # Closed four
        },
        3: {
            'open': 5000,     # Open three (major threat)
            'closed': 1000,   # Closed three
            'blocking': 7500  # Blocking opponent's 3 in a row
        },
        2: {
            'open': 500,      # Open two
            'closed': 100     # Closed two
        }
    }
    
    for row in range(ROWS):
        for col in range(COLS):
            if state.board[row][col] is None:
                continue
            
            for dr, dc in directions:
                sequence, gap_position, is_double_open = get_sequence(state.board, row, col, dr, dc)
                if not sequence:
                    continue
                
                length = len(sequence)
                current_player = sequence[0]
                
                if row > 0 and col > 0:
                    prev_r, prev_c = row - dr, col - dc
                    if (0 <= prev_r < ROWS and 0 <= prev_c < COLS and 
                        state.board[prev_r][prev_c] == current_player):
                        continue
                
                pattern_type = 'open' if is_double_open else 'closed'
                
                # Calculate pattern score
                if length >= 5:
                    pattern_score = weights[5]
                elif length >= 4:
                    pattern_score = weights[4][pattern_type]
                elif length >= 3:
                    # Modified logic for three-in-a-row patterns
                    if is_double_open:
                        if current_player != player:
                            # If it's opponent's three in a row and double open,
                            # consider it as blocking priority
                            pattern_score = weights[3]['blocking']
                        else:
                            pattern_score = weights[3]['open']
                    else:
                        pattern_score = weights[3][pattern_type]
                elif length >= 2:
                    pattern_score = weights[2][pattern_type]
                else:
                    continue
                
                # Adjust scores for opponent's threats
                if current_player != player:
                    if length >= 4:
                        pattern_score *= 1.2
                    if is_double_open and length >= 3:
                        pattern_score *= 1.1
                
                multiplier = 1 if current_player == player else -1
                score += multiplier * pattern_score
                
                # Add position bonus
                center_row, center_col = ROWS // 2, COLS // 2
                distance_to_center = abs(row - center_row) + abs(col - center_col)
                position_bonus = 50 * (1 / (distance_to_center + 1))
                score += position_bonus * multiplier
    
    return score

def get_sequence(board, row, col, dr, dc):
    sequence = []
    player = board[row][col]
    
    # Check backwards first to find start of sequence
    r, c = row - dr, col - dc
    backwards_empty = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] is None:
        backwards_empty += 1
        r, c = r - dr, c - dc
    
    # Now check forwards
    r, c = row, col
    gap_found = False
    gap_position = None
    forwards_empty = 0
    
    for i in range(5):
        if not (0 <= r < ROWS and 0 <= c < COLS):
            break
        
        current = board[r][c]
        if current == player:
            sequence.append(current)
        elif current is None and not gap_found:
            gap_found = True
            gap_position = len(sequence)
            forwards_empty += 1
        elif current is None:
            forwards_empty += 1
            break
        else:
            break
        
        r, c = r + dr, c + dc
    
    is_double_open = (backwards_empty > 0 and forwards_empty > 0)
    return sequence, gap_position, is_double_open


def is_sequence_open(board, row, col, dr, dc):
    player = board[row][col]
    sequence_length = len(get_sequence(board, row, col, dr, dc))
    
    r, c = row - dr, col - dc
    before_open = (0 <= r < ROWS and 0 <= c < COLS and 
                  board[r][c] is None)
    
    r, c = row + (sequence_length * dr), col + (sequence_length * dc)
    after_open = (0 <= r < ROWS and 0 <= c < COLS and 
                 board[r][c] is None)
    
    if before_open and after_open:
        return 2
    elif before_open or after_open:
        return 1
    return 0

def minimax(state, depth, alpha, beta, maximizing_player, player):
    if depth == 0:
        return evaluate_position(state, player), None
        
    valid_moves = state.get_valid_moves()
    if not valid_moves:
        return 0, None
        
    best_move = random.choice(valid_moves)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            row, col = move
            new_state = GameState(state.board)
            new_state.board[row][col] = player
            
            eval, _ = minimax(new_state, depth - 1, alpha, beta, False, player)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
                
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    else:
        min_eval = float('inf')
        opponent = "white" if player == "black" else "black"
        for move in valid_moves:
            row, col = move
            new_state = GameState(state.board)
            new_state.board[row][col] = opponent
            
            eval, _ = minimax(new_state, depth - 1, alpha, beta, True, player)
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
                
            beta = min(beta, eval)
            if beta <= alpha:
                break
                
        return min_eval, best_move

def get_ai_move(board, current_player):
    state = GameState(board)
    _, move = minimax(state, MAX_DEPTH, float('-inf'), float('inf'), True, current_player)
    return move

def check_win(board, row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        start, end = (row, col), (row, col)
        
        # Check forward direction
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                end = (r, c)
            else:
                break
                
        # Check backward direction
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                start = (r, c)
            else:
                break
                
        if count >= 5:
            return start, end
    return None
