import json
import sys
import copy
#sys.setrecursionlimit(3000)
#player_0_wins = 1000000
#player_1_wins = -player_0_wins
class Board:
    def __init__(self, positions, moves = None, n_moves = 0, dificult=7 , combinations=None):
        self.positions = positions
        self.moves = moves
        self.n_moves = n_moves
        self.valid_moves = [0, 1, 2, 3, 4, 5, 6]
        self.valid_moves_array = [[0], [1], [2], [3], [4], [5], [6]]
        self.player_0_wins = 1000000
        self.player_1_wins = -self.player_0_wins
        self.allPossibilities = None
        self.dificult = dificult
        self.combinations = combinations
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
        return Board(new_positions, n_moves=self.n_moves, dificult=self.dificult)
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
    def fulfilTree(self, moves, n_player):
        # first player is 1(max) and second is -1(min)
        if(not moves):
            if(n_player>0):
                max_score = self.player_1_wins
                for i,child in enumerate(self.allPossibilities[1], start=0):
                    child_score = self.fulfilTree([i], n_player*(-1))
                    if(child_score>=max_score):
                        max_score = child_score
                    if(child[1]):
                        child.append(child_score)
                self.allPossibilities.append(max_score)
            else:
                min_score = self.player_0_wins
                for i,child in enumerate(self.allPossibilities[1], start=0):
                    child_score = self.fulfilTree([i], n_player*(-1))
                    if(child_score<=min_score):
                        min_score = child_score
                    if(child[1]):
                        child.append(child_score)
                self.allPossibilities.append(min_score)
        else:
            actual_node = self.allPossibilities
            for item in moves:
                actual_node = actual_node[1][item]
            if(not actual_node[1]):
                return actual_node[2]
            if(n_player>0):
                max_score = self.player_1_wins
                for i,child in enumerate(actual_node[1], start=0):
                    child_score = self.fulfilTree(moves+[i], n_player*(-1))
                    if(child_score>=max_score):
                        max_score = child_score
                    if(child[1]):
                        child.append(child_score)
                actual_node.append(max_score)
                return max_score
            else:
                min_score = self.player_0_wins
                for i,child in enumerate(actual_node[1], start=0):
                    child_score = self.fulfilTree(moves+[i], n_player*(-1))
                    if(child_score<=min_score):
                        min_score = child_score
                    if(child[1]):
                        child.append(child_score)
                actual_node.append(min_score)
                return min_score
    '''
    def fulfilTree(self, node, n_player):
        # first player is 1(max) and second is -1(min)
        if(not node[1]):
            return node[2]
        else:
            if(n_player>0):
                scores = []
                for child in node[1]:
                    scores.append(self.fulfilTree(child, n_player*(-1)))
                node.append(max(scores))
                return max(scores)
            else:
                scores = []
                for child in node[1]:
                    scores.append(self.fulfilTree(child, n_player*(-1)))
                node.append(min(scores))
                return min(scores)
    '''
    '''         
    def applyScore(self):   
        print("Aplicando score nos movimentos...")
        for possibility in self.allPossibilities:
            possibility = self.simulateMovesWithScore(possibility)
    '''
    '''
    def generatePossibleMoves(self, n_moves):
        print("Gerando movimentos possíveis...")
        
        all_possibilities = self.getAllPossibilities(self.valid_moves_array, self.valid_moves, n_moves-1)
        #for index, possibilitie in enumerate(all_possibilities, start=0):
            #if(not self.validate_moves(possibilitie)):
                #all_possibilities.pop(index)
        self.allPossibilities = all_possibilities
        return all_possibilities
    '''
    def generatePossibleMoves(self):
        #print("Gerando movimentos possíveis...")
        
        
        #for index, possibilitie in enumerate(all_possibilities, start=0):
            #if(not self.validate_moves(possibilitie)):
                #all_possibilities.pop(index)
        #self.filterPossibilities(all_possibilities, self.getNewInstance())
        #self.allPossibilities = self.getAllPossibilities([None, []], self.valid_moves, self.dificult-1)
        #print("filtrando possibilidades...")
        self.filterPossibilities([])
        #print("Operação finalizada")
    def filterPossibilities(self, moves):
        if(not moves):
            deleted= False
            count = 0
            for i,child in enumerate(self.allPossibilities[1], start=0):
                new_board = self.getNewInstance()
                if(not new_board.dropCell(child[0])):
                    deleted = True
                    count+=1
                    self.allPossibilities[1][i] = False
                else:
                    score = new_board.getScore() 
                    if(score==new_board.player_0_wins or score==new_board.player_1_wins):
                        child[1].clear()
                        child.append(score)
                    else:
                        if(child[1]):
                            self.filterPossibilities(moves+[(i, child[0])])
                        else:
                            child.append(score)
            if(deleted):
                for x in range(0, count):
                    self.allPossibilities[1].remove(False)
        else:
            actual_node = self.allPossibilities
            for item in moves:
                actual_node = actual_node[1][item[0]]
            deleted= False
            count = 0
            for i,child in enumerate(actual_node[1], start=0):
                new_board = self.getNewInstance()
                for move in moves:
                    new_board.dropCell(move[1])
                if(not new_board.dropCell(child[0])):
                    deleted = True
                    count+=1
                    actual_node[1][i] = False
                else:
                    score = new_board.getScore() 
                    if(score==new_board.player_0_wins or score==new_board.player_1_wins):
                        child[1].clear()
                        child.append(score)
                    else:
                        if(child[1]):
                            self.filterPossibilities(moves+[(i, child[0])])
                        else:
                            child.append(score)
            if(deleted):
                for x in range(0, count):
                    actual_node[1].remove(False) 
     
    '''
    def filterPossibilities(self, node, board):
        deleted= False
        count = 0
        for i,child in enumerate(node[1], start=0):
            new_board = board.getNewInstance()
            if(not new_board.dropCell(child[0])):
                deleted = True
                count+=1
                node[1][i] = -1
            else:
                score = new_board.getScore() 
                if(score==new_board.player_0_wins or score==new_board.player_1_wins):
                    child[1].clear()
        if(deleted):
            for count in range(0, count):
                node[1].remove(-1)
        for child in node[1]:
            new_board = board.getNewInstance()
            new_board.dropCell(child[0])
            self.filterPossibilities(child, new_board)
    '''
    '''
    def getAllPossibilities(self, node, controll, n):
        if(n<0):
            return node 
        for element in controll:
            node[1].append(self.getAllPossibilities([element, []], controll, n-1))
        return node
    '''
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
        #self.filterPossibilities()
        return data
def play(board, node, n_player=1):
    if(n_player>0):
        if(len(node[1])==0):
            if(board.n_moves%2==0):
                player_multiplier = 1  
            else:
                player_multiplier = -1
            #board.filterPossibilities(board.allPossibilities, board.getNewInstance())
            board.generatePossibleMoves()
            board.applyScore(board.allPossibilities, board.getNewInstance())
            #with open('data.json', 'w+') as outfile:
                #json.dump(board.allPossibilities, outfile)
            #board.fulfilTree(board.allPossibilities, n_player)
            board.fulfilTree([], player_multiplier)
            node = board.allPossibilities

            
            move = board.chooseMove(node, player_multiplier)
            board.dropCell(node[1][move][0])
            board.printBoard()
            actual_score = board.getScore()
            
            if(actual_score==board.player_0_wins):
                print('\33[41m'+"O jogador 0 venceu!"+'\x1b[0m')
                board.printBoard(0)
            elif(actual_score==board.player_1_wins):
                print('\33[42m'+"O jogador 1 venceu!"'\x1b[0m')
                board.printBoard(1)
            else:
                play(board, node[1][move], n_player*(-1))
        else:
            #board.generatePossibleMoves()
            #board.applyScore(board.allPossibilities, board.getNewInstance())
            #with open('data.json', 'w+') as outfile:
                #json.dump(board.allPossibilities, outfile)
            #board.fulfilTree(board.allPossibilities, n_player)
            #board.fulfilTree([], n_player)
            #node = board.allPossibilities
            if(board.n_moves%2==0):
                move = board.chooseMove(node, 1)
            else:
                move = board.chooseMove(node, -1)
            board.dropCell(node[1][move][0])
            board.printBoard()
            actual_score = board.getScore()
            if(actual_score==board.player_0_wins):
                print('\33[41m'+"O jogador 0 venceu!"+'\x1b[0m')
                board.printBoard(0)
            elif(actual_score==board.player_1_wins):
                print('\33[42m'+"O jogador 1 venceu!"'\x1b[0m')
                board.printBoard(1)
            else:
                #print(move)
                #print(node[1][move])
                play(board, node[1][move], n_player*(-1))
            
    else:
        if(len(node[1])==0):
            if(board.n_moves%2==0):
                player_multiplier = 1  
            else:
                player_multiplier = -1
            #board.filterPossibilities(board.allPossibilities, board.getNewInstance())
            board.generatePossibleMoves()
            board.applyScore(board.allPossibilities, board.getNewInstance())
            #with open('data.json', 'w+') as outfile:
                #json.dump(board.allPossibilities, outfile)
            #board.fulfilTree(board.allPossibilities, n_player)
            board.fulfilTree([], player_multiplier)
            node = board.allPossibilities

            move = int(input("Faça sua jogada: "))
            index = -1
            for i, child in enumerate(node[1], start=0):
                if(child[0]==move):
                    index = i
            board.dropCell(move)
            actual_score = board.getScore()
            if(actual_score==board.player_0_wins):
                print('\33[41m'+"O jogador 0 venceu!"+'\x1b[0m')
                board.printBoard(0)
            elif(actual_score==board.player_1_wins):
                print('\33[42m'+"O jogador 1 venceu!"'\x1b[0m')
                board.printBoard(1)
            else:
                board.printBoard()
                play(board, node[1][index], n_player*(-1))
        else:
            move = int(input("Faça sua jogada: "))
            index = -1
            for i, child in enumerate(node[1], start=0):
                #print(i)
                #print(child)
                if(child[0]==move):
                    index = i
            board.dropCell(move)
            actual_score = board.getScore()
            if(actual_score==board.player_0_wins):
                print('\33[41m'+"O jogador 0 venceu!"+'\x1b[0m')
                board.printBoard(0)
            elif(actual_score==board.player_1_wins):
                print('\33[42m'+"O jogador 1 venceu!"'\x1b[0m')
                board.printBoard(1)
            else:
                board.printBoard()
                play(board, node[1][index], n_player*(-1))
            



positions = [[0 for x in range(0, 7)] for y in range(0, 6)] 
for y in range(0, 6):
    for x in range(0, 7):
        positions[y][x] = [None, None]
board = Board(positions, dificult=7)
board.printBoard()


'''
board.dropCell(3)
#board.printBoard()
board.dropCell(3)
board.dropCell(3)
board.dropCell(3)
board.dropCell(0)
board.dropCell(6)

board.dropCell(0)
board.dropCell(2)
board.printBoard()
board.dropCell(1)
board.dropCell(2)
board.dropCell(1)
board.dropCell(2)
board.dropCell(2)
board.dropCell(4)
board.dropCell(0)
#board.printBoard()
board.dropCell(0)
board.dropCell(1)
board.dropCell(1)
board.dropCell(2)
board.dropCell(2)
board.dropCell(4)
board.printBoard()
'''
board.printBoard()
#print(board.getScore())
#print(board.positions)
print("gerando")
#board.generatePossibleMoves()
#all_conbinations = board.loadMovesFromJson() 
#board.applyScore(board.allPossibilities, board.getNewInstance())
#board.fulfilTree(board.allPossibilities, 1)
#board.fulfilTree([], 1)
#with open('data.json', 'w+') as outfile:
    #json.dump(board.allPossibilities, outfile)
#print(len(board.allPossibilities))
#board.getAllPossibilities()
board.generateCombinations()
board.scoreEdge()
print("fim")
#print(len(board.allPossibilities))
#print(len(board.allPossibilities[-1]))
#print(board.allPossibilities)
#play(board, board.allPossibilities, -1)