import json
import sys
import copy
sys.setrecursionlimit(5000)
#player_0_wins = 1000000
#player_1_wins = -player_0_wins
class Board:
    def __init__(self, positions, moves = None, n_moves = 0, dificult=7 , combinations=None, alpha=-1000000, beta=1000000, parent_move=None):
        self.positions = positions
        self.moves = moves
        self.n_moves = n_moves
        self.valid_moves = [0, 1, 2, 3, 4, 5, 6]
        self.valid_moves_array = [[0], [1], [2], [3], [4], [5], [6]]
        self.player_0_wins = 1000000
        self.player_1_wins = -self.player_0_wins
        self.dificult = dificult
        self.combinations = combinations
        self.avaliable_moves = [0, 1, 2, 3, 4, 5, 6]
        self.isLeaf = False
        self.tree = None
        self.alpha = [alpha, parent_move]
        self.beta = [beta, parent_move]
        self.parent_move = parent_move
        self.best_move = None
        self.generated_childs = 0
    def setParentMove(self, move):
        self.alpha[1] = move
        self.beta[1] = move
        self.parent_move = move
    def printBoard(self, winner=-1):
        #-1 -> no winner
        # 0 -> player 0 wins
        # 1 -> player 1 wins
        if(winner==-1):
            print('')
            print('_ _  _  _  _  _  _  _ _')
            for y in range(0, 6):
                for x in range(0, 7):
                    if(x==0):
                        print('|', end='')
                    if(self.positions[y][x][0] is None):
                        print('   ', end='')
                    elif(self.positions[y][x][0] == 1):
                        print('\033[32m'+' 1 '+'\x1b[0m', end='')
                    else:
                        print('\033[91m'+' 0 '+'\x1b[0m', end='')
                    if(x==6):
                        print('|')
                    
            print('_ _  _  _  _  _  _  _ _')
            print('')
            print('_ 0  1  2  3  4  5  6 _')
            print('')
        elif(winner==0):
            print('')
            print('_ _  _  _  _  _  _  _ _')
            for y in range(0, 6):
                for x in range(0, 7):
                    if(x==0):
                        print('|', end='')
                    if(self.positions[y][x][0] is None):
                        print('   ', end='')
                    elif(self.positions[y][x][0] == 1):    
                        print('\033[32m'+' 1 '+'\x1b[0m', end='')
                    else:
                        if(self.getCellScore(x,y)==self.player_0_wins):
                            print('\33[41m'+' 0 '+'\x1b[0m', end='')
                        else:
                            print('\033[91m'+' 0 '+'\x1b[0m', end='')
                    if(x==6):
                        print('|')
                    
            print('_ _  _  _  _  _  _  _ _')
            print('')
            print('_ 0  1  2  3  4  5  6 _')
            print('')
        elif(winner==1):
            print('')
            print('_ _  _  _  _  _  _  _ _')
            for y in range(0, 6):
                for x in range(0, 7):
                    if(x==0):
                        print('|', end='')
                    if(self.positions[y][x][0] is None):
                        print('   ', end='')
                    elif(self.positions[y][x][0] == 1):    
                        if(self.getCellScore(x,y)==self.player_0_wins):
                            print('\33[42m'+' 1 '+'\x1b[0m', end='')
                        else:
                            print('\033[32m'+' 1 '+'\x1b[0m', end='')
                    else:
                        print('\033[91m'+' 0 '+'\x1b[0m', end='')
                    if(x==6):
                        print('|')
                    
            print('_ _  _  _  _  _  _  _ _')
            print('')
            print('_ 0  1  2  3  4  5  6 _')
            print('')
    def dropCell(self, position):
        cont = 5
        for y in range(0, 6):
            if(self.positions[y][position][0] is not None):
                cont-=1
        if(cont==-1):
            return False
        self.positions[cont][position] = [(self.n_moves%2), self.n_moves+1]
        self.n_moves+=1
        return True
    def chooseMove(self, node, n_player):
        if(n_player>0):
            greater = self.player_1_wins
            move = None
            for index,child in enumerate(node[1], start=0):
                if(child[0] is None):
                    continue
                if(child[2]>=greater):
                    greater = child[2]
                    move = index
            return move
        else:
            smaller = self.player_0_wins
            move = None
            for index, child in enumerate(node[1], start=0):
                if(child[0] is None):
                    continue
                if(child[2]<=smaller):
                    smaller = child[2]
                    move = index
            return move
    def getNewInstance(self):
        new_positions = [[0 for x in range(0, 7)] for y in range(0, 6)] 
        for y in range(0, 6):
            for x in range(0, 7):
                new_positions[y][x] = self.positions[y][x]
        return Board(new_positions, n_moves=self.n_moves, dificult=self.dificult, alpha= self.alpha[0], beta= self.beta[0])
    def format(self, v1, v2):    
        combinations = []
        for e in v1:
            for element in v2:
                combinations.append(e+[element])
        return combinations
    def getCombinations(self, v1, v2, n):
        if n == 0:
            return v1
        result = []
        for element in v1:
            result+=self.format([element], v2)
        return self.getCombinations(result, v2, n-1)
    def generateCombinations(self):
        self.combinations = self.getCombinations(self.valid_moves_array, self.valid_moves, self.dificult-1)
    def scoreA(self, combination):
        new_tab = self.getNewInstance()
        valid_moves = []
        for move in combination:
            if(new_tab.dropCell(move)):
                score = new_tab.getScore()
                if(score==self.player_0_wins or score==self.player_1_wins):
                    valid_moves.append([move, -1])
                    break
                else:
                    valid_moves.append(move)
            else:
                print('x')
                break
        return valid_moves
                
    def scoreEdge(self):
        for combination in self.combinations:
            combination = self.scoreA(combination)
    def checkUp(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(y>2):
            for n in range(y, y-4, -1):
                if(self.positions[n][x][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkDown(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(y<3):
            for n in range(y, y+4):
                if(self.positions[n][x][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkLeft(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(x>2):
            for n in range(x, x-4, -1):
                if(self.positions[y][n][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkRight(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(x<4):
            for n in range(x, x+4):
                if(self.positions[y][n][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkUpRight(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(y>2 and x<4):
            for n in range(0, 4):
                if(self.positions[y-n][x+n][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkDownRight(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(y<3 and x<4):
            for n in range(0, 4):
                if(self.positions[y+n][x+n][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkUpLeft(self, x, y):
        score = 0
        player_number = self.positions[y][x][0] 
        if(y>2 and x>2):
            for n in range(0, 4):
                if(self.positions[y-n][x-n][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def checkDownLeft(self, x, y):
        score = 0
        player_number = self.positions[y][x][0]
        if(y<3 and x>2):
            for n in range(0, 4):
                if(self.positions[y+n][x-n][0] == player_number):
                    score+=1
            return score
        else:
            return 0
    def getCellScore(self, x, y):
        scoreUp = self.checkUp(x, y)
        scoreDown = self.checkDown(x, y)
        scoreLeft = self.checkLeft(x, y)
        scoreRight = self.checkRight(x, y)
        scoreUpRight = self.checkUpRight(x, y)
        scoreUpLeft = self.checkUpLeft(x, y)
        scoreDownRight = self.checkDownRight(x, y)
        scoreDownLeft = self.checkDownLeft(x, y)

        if(scoreUp==4 or scoreDown==4 or scoreLeft==4 or scoreRight==4 or scoreUpRight==4 or scoreUpLeft==4 or scoreDownRight==4 or scoreDownLeft==4):
            return self.player_0_wins # this return just say that some player wins 
        return scoreUp + scoreDown + scoreLeft + scoreRight + scoreUpRight + scoreUpLeft + scoreDownRight + scoreDownLeft
    def getScore(self):
        #reimplementar
        board_score = 0
        for y in range(0, 6):
            for x in range(0, 7):
                if(self.positions[y][x][0] is None):
                    continue
                player_multiplier = 0
                if(self.positions[y][x][0] == 0):
                    player_multiplier = 1
                else:
                    player_multiplier = -1
                actual_score = (self.getCellScore(x, y)*player_multiplier)
                if(actual_score == self.player_1_wins):
                    return self.player_1_wins
                elif(actual_score == self.player_0_wins):
                    return self.player_0_wins
                board_score+= actual_score
                #print(actual_score)
        return board_score
    def validate_moves(self, moves):
        new_board = self.getNewInstance()
        for move in moves:
            if(not new_board.dropCell(move)):
                return False
        return True
    def applyScore(self, node, board):
        if(node[0] is None):
            for child in node[1]:
                new_board = board.getNewInstance()
                self.applyScore(child, new_board)
        elif(board.dropCell(node[0])):
            if(not node[1]):
                #print("y")
                node.append(board.getScore())
            else:
                for child in node[1]:
                    new_board = board.getNewInstance()
                    self.applyScore(child, new_board)
    def getAllChilds(self):
        childs = []
        for move in self.valid_moves:
            new_board = self.getNewInstance()
            if(new_board.dropCell(move)):
                childs.append(new_board)
        return childs
    def getAllPossibilities(self):
        all = [[self]]
        for count in range(0, self.dificult):
            new_depth = []
            for node in all[-1]:
                score = node.getScore() 
                if(score==self.player_0_wins or score == self.player_1_wins):
                    continue
                new_depth.extend(node.getAllChilds())
            all.append(new_depth)
        self.allPossibilities = all
        
    def loadMovesFromJson(self):
        with open('data.json', 'r') as myfile:
            data = json.loads(myfile.read())
        self.allPossibilities = data
        return data
    def getChild(self):
        remove = []
        use = []
        new_board = None
        for i,move in enumerate(self.avaliable_moves, start=0):
            new_board = self.getNewInstance()
            if(new_board.dropCell(self.avaliable_moves[i])):
                score = new_board.getScore() 
                if(score==self.player_0_wins or score==self.player_1_wins):
                    new_board.avaliable_moves = []
                new_board.setParentMove(self.avaliable_moves[i])
                remove.append(i)
                use.append(i)
                break
            else:
                remove.append(i)
        for removed, i in enumerate(remove, start=0):
            self.avaliable_moves.pop(i-removed)
        if(len(use)==0):
            return False
        else:
            self.generated_childs+=1
            return new_board   
    def alphabeta(self):
        count = 0
        while(len(self.tree[0].avaliable_moves)>0 or len(self.tree)!=1):
            if(self.tree[-1].alpha[0]>=self.tree[-1].beta[0] and len(self.tree)>1):
                self.tree.pop(-1)
                continue
            count+=1
            # go to leaf node
            while(len(self.tree)<=self.dificult):
                child = self.tree[-1].getChild()
                if(child):
                    self.tree.append(child)
                else:
                    break
            if(len(self.tree)==1):
                return "fim"
            if(self.tree[-1].generated_childs>0):
                if(self.tree[-1].n_moves%2==0):
                    if(self.tree[-1].alpha[0]<self.tree[-2].beta[0]):
                        self.tree[-2].beta[0] = self.tree[-1].alpha[0]
                        self.tree[-2].best_move = self.tree[-1].parent_move
                else:
                    if(self.tree[-1].beta[0]>self.tree[-2].alpha[0]):
                        self.tree[-2].alpha[0] = self.tree[-1].beta[0]
                        self.tree[-2].best_move = self.tree[-1].parent_move
                self.tree.pop(-1)
                continue
            else:
                score = self.tree[-1].getScore()
                if(self.tree[-1].n_moves%2==0):
                    if(score<self.tree[-2].beta[0]):
                        self.tree[-2].beta[0] = score
                        self.tree[-2].best_move = self.tree[-1].parent_move
                else:
                    if(score>self.tree[-2].alpha[0]):
                        self.tree[-2].alpha[0] = score
                        self.tree[-2].best_move = self.tree[-1].parent_move
                self.tree.pop(-1)
                continue
        print(count)
            
    def minimax(self):
        self.tree = [self.getNewInstance()]
        return self.alphabeta()
        #return self.tree[0].best_move

def play(board, human_player_turn=True):
    if(human_player_turn):
        print("Sua jogada: ")
        move = int(input())
        board.dropCell(move)
        board.printBoard()
        score = board.getScore()
        if(score==board.player_0_wins):
            print("O jogador 0 venceu!")
            return True
        elif(score==board.player_1_wins):
            print("O jogador 1 venceu!")
            return True
        play(board, not human_player_turn)
    else:
        board.minimax()
        move = board.tree[0].best_move
        board.dropCell(move)
        board.printBoard()
        score = board.getScore()
        if(score==board.player_0_wins):
            print("O jogador 0 venceu!")
            return True
        elif(score==board.player_1_wins):
            print("O jogador 1 venceu!")
            return True
        play(board, not human_player_turn)


positions = [[0 for x in range(0, 7)] for y in range(0, 6)] 
for y in range(0, 6):
    for x in range(0, 7):
        positions[y][x] = [None, None]
board = Board(positions, dificult=6)

board.printBoard()
play(board, False)