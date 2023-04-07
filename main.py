import random
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem", "key.pem")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"message to users": "This is a fastAPI server"}

@app.post("/process_data")
async def process_data(data: dict):
    # ideal_move = foo(data)
    # response = JSONResponse(content=ideal_move)
    # response.headers["Access-Control-Allow-Origin"] = "*"
    # return {"ideal_move":ideal_move}
    ideal_move = await asyncio.to_thread(foo, data)
    response = JSONResponse(content={"ideal_move": ideal_move})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def isWinner(board, player):
    combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [
        0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for c in combinations:
        if board[c[0]] == player and board[c[1]] == board[c[2]] and board[c[2]] == player:
            return True
    return False

def minimax(board, player, players):
    availableSpots = [x for x in board if type(x) == int]
    if len(availableSpots) == 9:
        return [random.randint(0, 8)]
    if(isWinner(board, players[0])):
        return [-1,10]
    elif(isWinner(board, players[1])):
        return [-1, -10]
    elif(len(availableSpots) == 0):
        return [-1,0]
    
    moves = [] # collects all the moves for future evaluation
    
    for spot in availableSpots:
        move = [-1,-1] # collect 0-> spot and 1-> score
        move[0] = board[spot] # position
        board[spot] = player

        if (player == players[0]):
            result = minimax(board, players[1], players)
            move[1] = result[1]
        else:
            result = minimax(board, players[0], players)
            move[1] = result[1]
        
        board[spot] = move[0] # backtrack
        moves.append(move)
    
    idealMove = -1
    
    if player == players[0]:
        bestScore = -1000
        for i in range(len(moves)):
            # print(len(moves))
            if moves[i][1] > bestScore:
                bestScore = moves[i][1]
                idealMove = i
    else:
        worstScore = 1000
        for i in range(len(moves)):
            if moves[i][1] < worstScore:
                worstScore = moves[i][1]
                idealMove = i
    
    return moves[idealMove]

def play(board, human, ai):        
    spot2 = minimax(board, ai, [ai,human])
    return spot2[0]

def foo(obj):
    board = [obj[x] if obj[x]!="" else int(x) for x in obj.keys()]
    return play(board, 'u', 'b')

    