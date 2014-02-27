from ctypes import *
from HaPy import hsklAI #See https://github.com/sakana/HaPy/blob/master/README.md 
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

def getRow(n):
    return n/4

def getCol(n):
    return n%4

def parsePlayerNum():
    players = [-1,-1]
    for x in range(2):
        text = "Who is Player " + str(x+1) + " [0] Human, [1] Haskell, [2] C++: "
        aiNum = -1            
        while(not (-1 < aiNum < 3)):
            try:
                aiNum = int(raw_input(text))
            except ValueError:
                print "Out of Range or Not a Number"
        players[x] = aiNum
    return players

def win(board, player):
    player = (player + 1) % 2
    for square in board:
        if player == 0 and square < 0:
            return False
        if player == 1 and square > 0:
            return False
    return True

def displayBoard(board):
    lines = ""
    row = 1
    for counter in range(64):
        if counter % 8 == 0:
            lines = lines + '\n'
            row = (row + 1) % 2
        if counter % 2 == row:
            lines = lines + '_'
        elif board[counter/2] == 1:
            lines = lines + 'x'
        elif board[counter/2] == 2:
            lines = lines + 'X'
        elif board[counter/2] == -1:
            lines = lines + 'o'
        elif board[counter/2] == -2:
            lines = lines +'O'
        else:
            lines = lines +'_'
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
    if(playerType == 0): #human
        return getHumanMove()

    if currPlayer == 1:
        board = flipB(board)

    if playerType == 1: #haskell
        move = hsklAI.callAI(board)
    elif playerType == 2: #c++
        move = callCPPAI(board)

    if currPlayer == 1:
        move = flipM(move)
        board = flipB(board)
    return move

def validateMove(board, moves, player):
    if moves[0] < 0: return False
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
        print str(piece) + " " + str(move)
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
            print str(piece-7) + " " + str(tempBoard[move]) + " " + str(tempBoard[piece - 3 - offset]) + " " + str(getCol(piece))
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
        print "Eh, " + str(moves) + " failed" #place holder for move validation
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
    while not win(board, currPlayer):
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
        currPlayer = (currPlayer + 1) %2
    print "Player " + str((currPlayer + 1)%2) + " WINS"

checkers()
#board = [0,2,0,0,0,-1,-1,0,0,0,0,0,0,-1,-1,-1,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0]
#board = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
# print callCPPAI(board)
#print hsklAI.callAI(board)

