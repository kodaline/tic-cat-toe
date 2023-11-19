from cat.mad_hatter.decorators import tool, hook, plugin
from cat.log import log

marks = ['X', 'O']
player_mark_dict = {}
global game_started
global current_turn
global winner
winner = None
current_turn = ""
game_started = False
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
remaining_tiles = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
global first_move
first_move = ""
@hook
def agent_prompt_prefix(prefix, cat):
    prefix = """You are a friendly Cat that entertains a user with Tic Tac Toe.
    Tic-Tac-Toe is played on a three-by-three grid by two players, who alternately place the marks X and O in one of the nine spaces in the grid.
    Before the game starts, you ask the user for the mark they want to use.
    Before the game starts, ask who to move first.
    Never Print out game board.
    When it's your turn just answer with your move choice.
    """
    return prefix


@hook(priority=1)
def before_cat_sends_message(final_output, cat):
    global game_started
    global current_turn
    global first_move
    global winner
    log.error("--------------")
    log.error(final_output["content"])
    log.error("--------------")

    if game_started:
        current_ai_move  = [int(s) for s in final_output["content"] if s.isdigit()]
        log.error("--------------")
        log.error(current_ai_move)
        log.error("--------------")
        if  len(current_ai_move) != 0:
            current_turn = "ai"
            update_board(board, current_turn, current_ai_move[0] - 1)
            value_index = remaining_tiles.index(str(current_ai_move[0]))
            if len(remaining_tiles) != 0:
                remaining_tiles.pop(value_index)
            current_turn = "user"
        check_game_over()
    if game_started and first_move != "" and current_turn != "":
        final_output["content"] += f"""\n {print_board(board)}"""
        check_game_over()
    if len(remaining_tiles) == 0 or winner:
        final_output["content"] += f"\n{and_the_winner_is()}"
        #reset game
        #winner = None
        #game_started = False
        #current_turn = ""
        #first_move = ""
        #player_mark_dict = {}
        #board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        #remaining_tiles = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    log.error("----------before_cat_sends_message------------")
    log.error(board)
    log.error(game_started)
    log.error(first_move)
    log.error(player_mark_dict)
    log.error(remaining_tiles)
    log.error(winner)
    return final_output

@hook(priority=1)
def before_cat_reads_message(user_message_json, cat):
    global game_started
    global current_turn
    global first_move
    global winner

    if 'X' in user_message_json["text"] and not game_started:
        player_mark_dict["user"] = 'X'
        player_mark_dict["ai"] = 'O'
    elif 'O' in user_message_json["text"] and not game_started:
        player_mark_dict["user"] = 'O'
        player_mark_dict["ai"] = 'X'
    if 'you' in user_message_json["text"] and first_move == "" and not game_started:
        first_move = "ai"
        current_turn = "ai"
    elif 'me' in user_message_json["text"] and first_move == "" and not game_started:
        first_move = "user"
        current_turn = "user"
    if first_move and current_turn and len(player_mark_dict) != 0:
        log.error("STARTING GAME")
        game_started = True
    if game_started:
        current_user_move  = [int(s) for s in user_message_json["text"] if s.isdigit()]
        if  len(current_user_move) != 0 and game_started:
            current_turn = "user"
            update_board(board, current_turn, current_user_move[0] - 1)
            value_index = remaining_tiles.index(str(current_user_move[0]))
            if len(remaining_tiles) != 0:
                remaining_tiles.pop(value_index)
            current_turn = "ai"
        check_game_over()
    log.error("----------before_cat_reads_message------------")
    log.error(board)
    log.error(game_started)
    log.error(first_move)
    log.error(player_mark_dict)
    log.error(remaining_tiles)
    log.error(winner)
    return user_message_json

@hook(priority=1)
def agent_prompt_suffix(suffix, cat):
    global game_started
    global current_turn
    if game_started:
        # add current game board to agent input, and current_turn
        suffix = f"""
# Context

Remaining tiles: {remaining_tiles} the only possible tiles to choose on the board.
Use remaining tiles to choose your placing, but never talk about it.
Example of your answer can be: I choose 7.
"""
        if current_turn == "ai":
            suffix += f"""\n
It's your turn!
"""
        suffix += """\n
{episodic_memory}

{declarative_memory}

{tools_output}

## Conversation until now:{chat_history}
 - Human: {input}
 - AI:
"""
    return suffix

'''
Helper methods below.
'''
def update_board(board, turn, position):
    board[position] = player_mark_dict[turn]
    return board


def print_board(board):
    return f"""
     {board[0]} | {board[1]} | {board[2]}
    -----------
     {board[3]} | {board[4]} | {board[5]}
    -----------
     {board[6]} | {board[7]} | {board[8]}
    """

def check_winner():
    global winner
    global game_started
    winner_row = check_board_row()
    winner_column = check_board_column()
    winner_diagonal = check_board_diagonal()

    #Gets the winner
    if winner_row:
        winner = winner_row
    elif winner_column:
        winner = winner_column
    elif winner_diagonal:
        winner = winner_diagonal
    else: winner = None

def check_board_row():
    global game_started
    row1 = board[0] == board[1] == board[2]
    row2 = board[3] == board[4] == board[5]
    row3 = board[6] == board[7] == board[8]

    if row1 or row2 or row3:
        game_started = False
    if row1:
        return board[0]
    elif row2:
        return board[3]
    elif row3:
        return board[6]

def check_board_column():
    global game_started
    column1 = board[0] == board[3] == board[6]
    column2 = board[1] == board[4] == board[7]
    column3 = board[2] == board[5] == board[8]

    if column1 or column2 or column3:
        game_started = False
    if column1:
        return board[0]
    elif column2:
        return board[1]
    elif column3:
        return board[2]

def check_board_diagonal():
    global game_started
    diag1 = board[0] == board[4] == board[8]
    diag2 = board[2] == board[4] == board[6]

    if diag1 or diag2:
        game_started = False
    if diag1:
        return board[0]
    elif diag2:
        return board[2]


def check_tie():
    global game_started
    game_started = any(tile.isdigit() for tile in board)

def check_game_over():
    check_winner()
    check_tie()

def and_the_winner_is():
    global winner
    winner_name = ""
    for key in player_mark_dict:
        if player_mark_dict[key] == winner and winner is not None:
            winner_name = key
            break
    if winner_name == "user":
        winner_name = "you"
    elif winner_name == "ai":
        winner_name = "me"
    if winner == None:
        return "It's a Tie!"
    else:
        return f"The winner is {winner_name}!"

def reset_game():
    global winner
    winner = None
    global game_started
    game_started = False
    global current_turn
    current_turn = ""
    global first_move
    first_move = ""
    player_mark_dict = {}
    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    remaining_tiles = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    log.error("----------reset_game------------")
    log.error(board)
    log.error(game_started)
    log.error(first_move)
    log.error(player_mark_dict)
    log.error(remaining_tiles)
    log.error(winner)