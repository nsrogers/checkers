def parsePlayerNum():
    players = [-1,-1]
    for x in range(2):
        text = "Who is Player " + str(x+1) + " [0] Human, [1] Haskell, [2] C++: "
        aiNum = -1            
        while(not (-1 < aiNum < 3)):
            try:
                aiNum = int(raw_input(text))
            except ValueError:
                print "BADDDDDD!!!!!"
        players[x] = aiNum
    return players

def win(board, player):
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
        row = int(temp[0])
        col = int(temp[1])
        moves.append([row,col])
    return moves

def getHumanMove():
    inputS = raw_input("What would you like to move\n<PlaceX>,<PlaceY> <Dest1X>,<Dest1Y> [<Dest2X>,Dest2Y*...]\n")
    moves = cordsToMove(inputS)
    trueMoves = []
    for move in moves:
        if move[0] %2 == move[1] % 2:
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
        move = getHaskellMove(board)
    elif playerType == 2: #c++
        move = getCppMove(board)

    if currPlayer == 1:
        move = flipM(move)
        board = flipB(board)
    return move


def checkers():
    board = [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    players = parsePlayerNum()
    # Player 0 is positive, Player 1 is negative
    currPlayer = 0
    while not win(board, currPlayer):
        displayBoard(board)
        move = getMove(board, currPlayer, players[currPlayer])
        return

print getHumanMove()
temp = [1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
displayBoard(temp)
temp = flipB(temp)
displayBoard(temp)
#checkers()
