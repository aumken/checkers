"""Main file -- takes user input, updates gamestate."""

# imports

import pygame as pg #library
import functions #another file withing workspace

# constants

WIDTH: int = 512
HEIGHT: int = 512
DIMENSIONS: int = 8
SQUARE_SIZE: int = WIDTH // DIMENSIONS
MAX_FPS = 15
IMAGES = {} #dictionary


def imageLoad():
    """loads image into images dictionary"""
    IMAGES["w"] = pg.transform.scale(pg.image.load("images/w.png"), (SQUARE_SIZE, SQUARE_SIZE)) #scale x,y
    IMAGES["b"] = pg.transform.scale(pg.image.load("images/b.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES["wK"] = pg.transform.scale(pg.image.load("images/wK.png"), (SQUARE_SIZE, SQUARE_SIZE)) #scale x,y
    IMAGES["bK"] = pg.transform.scale(pg.image.load("images/bK.png"), (SQUARE_SIZE, SQUARE_SIZE))
    IMAGES["whitewin"] = pg.image.load("images/whitewin.png")
    IMAGES["blackwin"] = pg.image.load("images/blackwin.png")
    #[]subscription notation, to get value into dictionary or position in a list
    

def main():
    """set up game"""
    pg.init()
    imageLoad()
    pg.display.set_caption("checkers")

    screen = pg.display.set_mode((WIDTH, HEIGHT)) #create screen
    screen.fill(pg.Color("white"))

    clock = pg.time.Clock()
    gamestate = functions.GameState()
    playing = True
    selected = ()
    clicks = []
    possibleMoves = gamestate.legalMoves()
    winner = "none"
    
    while playing == True:

        if len(gamestate.gamelog) >= 1:
            lastmove = gamestate.gamelog[len(gamestate.gamelog) - 1]

        for action in pg.event.get(): #action
            if action.type == pg.QUIT:
                playing = False
            elif action.type == pg.MOUSEBUTTONDOWN:
                mouselocation = pg.mouse.get_pos()
                column = mouselocation[0] // SQUARE_SIZE #x location is 0th index
                row = mouselocation[1] // SQUARE_SIZE
                drawGameState(screen, clicks, gamestate, selected, possibleMoves, winner)
                if selected == (row, column):
                    selected = ()
                    clicks = []
                else:
                    selected = (row, column)
                    clicks.append(selected)
                    drawGameState(screen, clicks, gamestate, selected, possibleMoves, winner)
                if len(clicks) == 1 and gamestate.board[clicks[0][0]][clicks[0][1]] == "..": #if there is one click and is equal to empty square
                    selected = () 
                    clicks = [] #clearing list of clicks
                if len(clicks) == 2:
                    move = functions.Move(clicks[0], clicks[1], gamestate.board)
                    selected = ()
                    clicks = []
                    for potentialMove in possibleMoves:
                        if move == potentialMove:
                            gamestate.makeMove(potentialMove)
                            possibleMoves = gamestate.legalMoves()
            elif action.type == pg.KEYDOWN and action.key == pg.K_LEFT:
                gamestate.undoMove()
                selected = ()
                clicks = []
        
        if gamestate.blackTurn:
            if possibleMoves == [] and (lastmove.piece != "b" or lastmove.piece != "bK"):
                winner = "white"
        else:
            if possibleMoves == [] and (lastmove.piece != "w" or lastmove.piece != "wK"):
                winner = "black"

        possibleMoves = gamestate.legalMoves()
        drawGameState(screen, clicks, gamestate, selected, possibleMoves, winner)
        clock.tick(MAX_FPS)
        pg.display.flip()
                

def drawGameState(screen, clicks, gamestate, selected, possibleMoves, winner):
    drawBoard(screen, clicks)
    drawPieces(screen, gamestate.board)
    drawPotentialMoves(screen, selected, gamestate, possibleMoves)
    drawGameOver(screen, winner)


def drawBoard(screen, clicks):
    colors = [pg.Color("burlywood"), pg.Color("burlywood4")]

    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color = colors[((row + column) % 2)]
            pg.draw.rect(screen, color, pg.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    if clicks != [] and len(clicks) != 2:
        pg.draw.rect(screen, pg.Color("red"), pg.Rect(clicks[0][1] * SQUARE_SIZE, clicks[0][0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            piece = board[row][column]
            if piece != "..":
                screen.blit(IMAGES[piece], pg.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPotentialMoves(screen, selected, gamestate, possibleMoves):
    if len(selected) >= 1:
        for move in possibleMoves:
            if move.startrow == selected[0] and move.startcolumn == selected[1]:
                pg.draw.circle(screen, pg.Color("red"), ((move.endcolumn * SQUARE_SIZE) + SQUARE_SIZE // 2, (move.endrow * SQUARE_SIZE) + SQUARE_SIZE // 2), 10)


def drawGameOver(screen, winner):
    if winner == "white":
        screen.blit(pg.transform.smoothscale(IMAGES["whitewin"], (394, 96)), (64, 202))

    if winner == "black":
        screen.blit(pg.transform.smoothscale(IMAGES["blackwin"], (394, 96)), (64, 202))


if __name__ == "__main__":
    main()