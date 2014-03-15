from ctypes import *
import time
from HaPy import hsklAI 
#See https://github.com/sakana/HaPy/blob/master/README.md 
#for directions on how to use HaPY. 

#pass in a list of ints
def callCPPAI(board):
    arr = (c_int * len(board))(*board)
    aiMove = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    aiMovePassed = (c_int * len(aiMove))(*aiMove)
    ai = CDLL("cpp_code.so").callAI
    ai.restype = POINTER(c_int * len(board))
    newBoard = ai(arr, aiMovePassed).contents
    tempMoveList = [newBoard[i] for i in range(len(newBoard))]
    retMove = []
    for j in tempMoveList:
        if j != -1:
            retMove.append(j)
        else:
            break
    return retMove

def callRandomAI(board):
    arr = (c_int * len(board))(*board)
    aiMove = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    aiMovePassed = (c_int * len(aiMove))(*aiMove)
    ai = CDLL("cpp_code.so").callRandomAI
    ai.restype = POINTER(c_int * len(board))
    newBoard = ai(arr, aiMovePassed).contents
    tempMoveList = [newBoard[i] for i in range(len(newBoard))]
    retMove = []
    for j in tempMoveList:
        if j != -1:
            retMove.append(j)
        else:
            break
    return retMove


def getRow(n):
    return n/4

def getCol(n):
    return n%4

def parsePlayerNum():
    players = [-1,-1]
    for x in range(2):
        text = "Who is Player " + str(x+1) + " [0] Human, [1] Haskell, [2] C++ [3] Random: "
        aiNum = -1            
        while(not (-1 < aiNum < 4)):
            try:
                aiNum = int(raw_input(text))
            except ValueError:
                print "Out of Range or Not a Number"
        players[x] = aiNum
    return players

def win(board,player):
    return win1v1(board,player) or winnomove(board,player)

def win1v1(board, player):
    for square in board:
        if player == 0 and square > 0:
            return False
        if player == 1 and square < 0:
            return False
    return True
    
def winnomove(board,player):
    for i in range(32):
        for j in [-9,-7,-5, -4, -3, 3, 4, 5, 7, 9]:
            if player == 0 and board[i] < 0:
                if validateMove(board, [i, i+j], 1):
                    return False
            if player == 1 and board[i] > 0:
                if validateMove(board, [i, i+j], 0):
                    return False
    return True

def draw(board, count, value):
    numPos = 0
    numNeg = 0
    print count
    for i in board:
        if i > 0:
            numPos = numPos + i
        if i < 0:
            numNeg = numNeg + i
    if numPos + numNeg == value:
        count = count + 1
    else:
        count = 1
    value = numPos + numNeg
    if numPos == 1 and numNeg == 1:
        return True, count, value
    elif count == 100: 
        return True, count, value
    else:
        return False, count, value

def displayBoard(board):
    row = 1
    lines = "   1 2 3 4 5 6 7 8"
    for counter in range(64):
        if counter % 8 == 0:
            lines = lines + '\n'
            row = (row + 1) % 2
            lines = lines + str(getRow(counter/2) + 1) + "  "
        if counter % 2 == row:
            lines = lines + '_ '
        elif board[counter/2] == 1:
            lines = lines + 'x '
        elif board[counter/2] == 2:
            lines = lines + 'X '
        elif board[counter/2] == -1:
            lines = lines + 'o '
        elif board[counter/2] == -2:
            lines = lines +'O '
        else:
            lines = lines +'_ '
    print lines        


def flipB(board):
    for square in range(len(board)):
        board[square] = -1 * board[square]
    board.reverse()
    return board

def flipM(move):
    for x in range(len(move)):
        move[x] = 31 - move[x]
    return move

def cordsToMove(inputS):
    moves = []
    for x in inputS.split(" "):
        temp = x.split(",")
        if(len(temp)!=2): return [[-1,-1]]
        row = int(temp[0]) #Catch valueERROR
        col = int(temp[1])
        if not((0 < row < 9)) or not((0 < col < 9)):
           return [[-1,-1]]
        moves.append([row,col])
    return moves

def getHumanMove():
    inputS = raw_input("What would you like to move\n<PlaceRow>,<PlaceCol> <Dest1Row>,<Dest1Col> [<Dest2Row>,<Dest2Col> ...]\n")
    moves = cordsToMove(inputS)
    trueMoves = []
    for move in moves:
        if (move[0] %2 == move[1] % 2) or move[0] < 0 or move[1] < 0:
            return [-1]
        trueMoves.append(((move[0]-1)*4)+(move[1]-1)/2)	
    return trueMoves

def getMove(board, currPlayer, playerType):
    move = []
    start = time.time()
    if(playerType == 0): #human
        move = getHumanMove()
        print "Human Time: " + str(time.time() - start) + " s"
        return move

    if currPlayer == 1:
        board = flipB(board)
        
    if playerType == 1: #haskell
        move = hsklAI.callAI(board)
        print "Haskell AI Time: " + str(time.time() - start) + " s"
    elif playerType == 2: #c++
        move = callCPPAI(board)
        print "CPP AI Time: " + str(time.time() - start) + " s"
    elif playerType == 3:
        move = callRandomAI(board)
        print "Random AI Time: " + str(time.time() - start) + " s"
    if currPlayer == 1:
        move = flipM(move)
        board = flipB(board)
    return move

def validateMove(board, moves, player):
    for move in moves:
        if not (0 <= move <= 31): return False
    tempBoard = board[:]
    if player == 1:
        tempBoard = flipB(board[:])
        moves = flipM(moves[:])
  #      return True
    piece = moves[0]
    move = moves[1]
    offset = getRow(piece) % 2;
    if (move==(piece+4 - offset)) and (tempBoard[move] == 0 and (piece % 8 != 4)): # down left
        return True
    if (move==(piece+5 - offset)) and (tempBoard[move] == 0 and (piece % 8 != 3)): # down right
        return True
    if(tempBoard[piece]>1):
        if (move==(piece-3 - offset)) and (tempBoard[move] == 0 and (piece % 8 != 3)): #up right
            return True
        if (move==(piece-4 - offset)) and (tempBoard[move] == 0 and (piece % 8 != 4)): # up left
            return True
                 
    for move in moves[1:]:
        offset = getRow(piece) % 2;
        if (move==(piece+7)) and (tempBoard[move] == 0) and (tempBoard[piece+4 - offset]<0 and
                getCol(piece) != 0): #jump down left
            applyMove(tempBoard, [piece, move], 0)
            piece = move
            continue
        if (move==(piece+9)) and (tempBoard[move] == 0) and (tempBoard[piece+5 - offset]<0 and
                getCol(piece) != 34): #jump down right
            applyMove(tempBoard, [piece, move], 0)
            piece = move
            continue
        if(tempBoard[piece]>1):
            if (move==(piece-7)) and (tempBoard[move] == 0) and (tempBoard[piece-3 - offset]<0) and \
                    (getCol(piece) != 3): # jump right
                applyMove(tempBoard, [piece, move], 0)
                piece = move
                continue
            if (move==(piece-9)) and (tempBoard[move] == 0) and (tempBoard[piece-4 - offset]<0 and
                    getCol(piece) != 0): # jump left
                applyMove(tempBoard, [piece, move], 0)
                piece = move
                continue
#        print "Eh, " + str(moves) + " failed" #place holder for move validation
        return False
    return True

def applyMove(board, moves, player):
    print moves
    if player == 1:
        flipB(board)
        flipM(moves)
    srcIndex = moves[0]
    srcPiece = board[srcIndex]
    for move in moves[1:]:
        offset = getRow(srcIndex) % 2
        if (move==(srcIndex+7)):
            board[srcIndex+4 - offset]=0 #capture piece logic
        elif (move==(srcIndex+9)):
            board[srcIndex+5 - offset]=0 #capture piece logic
        elif (move==(srcIndex-7)):
            board[srcIndex-3 - offset]=0 #capture piece logic
        elif (move==(srcIndex-9)):
            board[srcIndex-4 - offset]=0 #capture piece logic

        board[srcIndex] = 0
        board[move]=srcPiece
        srcIndex = move
        srcPiece = board[srcIndex]
    for x in range(28,32):
        if board[x] == 1:
            board[x] = 2;
    if player == 1:
        flipB(board)
    return board    

def checkers():
    #board = [0,2,0,0,0,-1,-1,0,0,0,0,0,0,-1,-1,-1,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0]
    board = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    
    players = parsePlayerNum()
    # Player 0 is positive, Player 1 is negative
    currPlayer = 0
    count = 0
    value = 0
    _win = False
    _draw = False
    while (not _win) and (not _draw):
        time.sleep(.5)
        displayBoard(board)
        if currPlayer == 0:
            print "It is Player x's Turn"
        else:
            print "It is Player o's Turn"
        move = getMove(board, currPlayer, players[currPlayer])
        if(validateMove(board, move, currPlayer)):
            board = applyMove(board,move, currPlayer)
        else:
            print "Invalid Move"
            continue
        _win = win(board, currPlayer)
        _draw, count, value = draw(board, count, value)
        currPlayer = (currPlayer + 1) %2
    displayBoard(board)
    if _win:
        print "Player " + str((currPlayer + 1)%2) + " WINS"
    elif _draw:
        print "Draw"
    else:
        print "Game ended for unknown reasons"

checkers()
#board = [0,2,0,0,0,-1,-1,0,0,0,0,0,0,-1,-1,-1,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0]
#board = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
# print callCPPAI(board)
#print hsklAI.callAI(board)

