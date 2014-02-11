def parsePlayerNum():
    inputn = int(input("How many Human players?:"))
    players = (0,0)
    if inputn == 1: 
        players = (0,1)
    if inputn == 2: 
        players = (1,1)
    return players

def checkers():
    players = parsePlayerNum()

checkers()
