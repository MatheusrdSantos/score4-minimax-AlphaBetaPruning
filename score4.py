from Board import *
#player_0_wins = 1000000
#player_1_wins = -player_0_wins
def play(board, human_player_turn=True):
    board.resetAlphaBeta()
    if(board.n_moves==42):
        print("The game ended tied!")
        return True
    if(human_player_turn):
        print("Your move: ")
        move = int(input())
        board.dropCell(move)
        score = board.getScore()
        if(score==board.player_0_wins):
            board.printBoard(0)
            print('\033[91m'+"Player 0 wins!"+'\x1b[0m')
            return True
        elif(score==board.player_1_wins):
            board.printBoard(1)
            print('\033[32m'+"Player 1 wins!"+'\x1b[0m')
            return True
        board.printBoard()
        play(board, not human_player_turn)
        '''
        #board.dificult = 4
        board.minimax()
        move = board.tree[0].best_move
        print("beta:")
        print(board.tree[0].beta[0])
        print("alpha:")
        print(board.tree[0].alpha[0])
        board.dropCell(move)
        board.printBoard()
        score = board.getScore()
        if(score==board.player_0_wins):
            board.printBoard(0)
            print('\033[91m'+"Player 0 wins!"+'\x1b[0m')
            return True
        elif(score==board.player_1_wins):
            board.printBoard(1)
            print('\033[32m'+"Player 1 wins!"+'\x1b[0m')
            return True
        play(board, not human_player_turn)
        '''
    else:
        #board.dificult = 7
        board.minimax()
        move = board.tree[0].best_move
        print("beta:")
        print(board.tree[0].beta[0])
        print("alpha:")
        print(board.tree[0].alpha[0])
        board.dropCell(move)
        score = board.getScore()
        if(score==board.player_0_wins):
            board.printBoard(0)
            print('\033[91m'+"Player 0 wins!"+'\x1b[0m')
            return True
        elif(score==board.player_1_wins):
            board.printBoard(1)
            print('\033[32m'+"Player 1 wins!"+'\x1b[0m')
            return True
        board.printBoard()
        play(board, not human_player_turn)

def beginNewMatch():
    print("Choose the AI level: ")
    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")
    print("4 - Very hard")
    level = int(input())+2

    print("Who begins?")
    print("1 - Me")
    print("2 - AI")
    first_player = int(input())
    positions = [[0 for x in range(0, 7)] for y in range(0, 6)] 
    for y in range(0, 6):
        for x in range(0, 7):
            positions[y][x] = [None, None]
    board = Board(positions, dificult=level)

    board.printBoard()
    if(first_player==1):
        play(board, True)
    else:
        play(board, False)