import pygame as p
from Chess import ChessEngine
from Chess import SmartMoveFinder
from multiprocessing import Process, Queue
p.display.set_caption('Шахматы')
WIDTH = HEIGHT = 630
WIN_SIZE = 630, 630
SIZE = 600
DIMENSION = 8
SQ_SIZE = SIZE // DIMENSION
FPS = 40
IMAGES = {}
IMAGESFORSTART = {}
LIGHTBLUE = (132,196,192)
BLUE = (0,86,143)
WHITE = (255,255,255)
BACKGROUND = "GRAY"
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT
LTRS = 'ABCDEFGH'
colors = [BLUE, LIGHTBLUE]
screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
ranksToRows = { '1':7, "2":6, "3":5, "4":4,
                "5":3, "6":2, "7":1, "8": 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
filesToCols = { 'A':0, "B":1, "C":2, "D":3,
                "E":4, "F":5, "G":6, "H": 7}
colsToFiles = {v: k for k, v in filesToCols.items()}
n_lines = p.Surface((SQ_SIZE * SQ_SIZE, SQ_SIZE // 2))
n_rows = p.Surface((SQ_SIZE // 2, DIMENSION * SQ_SIZE))
fields = p.Surface((DIMENSION * SQ_SIZE, DIMENSION * SQ_SIZE))
boardSur = p.Surface((
    (2*n_rows.get_width() + fields.get_width()) + 27,
    (2*n_lines.get_height() + fields.get_height()) +27
))
RECT_WIDTH = 200
RECT_HEIGHT = 100
RECT_X = (WIDTH - RECT_WIDTH) // 2
RECT_Y = (HEIGHT - RECT_HEIGHT) // 2

def load_Images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    piecesForStart = ["wQ","bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    for pieceForStart in piecesForStart:
        IMAGESFORSTART[pieceForStart] = p.transform.scale(p.image.load("./Chess/images/" + pieceForStart + ".png"), (WIDTH //4*3 -30, HEIGHT//4*3))



def main():
    p.init()
    moveLogFont = p.font.SysFont('Arial', 20, False, False)
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    screen.fill(BACKGROUND)
    moveMade = False
    animate = False
    load_Images()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True
    playerTwo = True
    choiced = False
    choicedColor = 0
    # AIThinking = False
    # moveFinderProcess = None
    while running:

        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        if choiced == False:
            DrawChossingColor(screen)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN: # Реализация ходов через клики
                if not gameOver:
                    pos = p.mouse.get_pos()
                    x, y = pos
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8 or row >= 8: # Пользователь нажал на одну и ту же клетку 2 раза
                        sqSelected = () # отмена выбора
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn: #После второго клика
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                    if choiced == False:
                        DrawChossingColor(screen)
                        if x <= WIDTH // 4 * 3 - 30 and y <= HEIGHT:
                            print("Выбран цвет: белый")
                            choiced = True
                            choicedColor = 1
                        elif x > WIDTH // 4 * 3 - 30 and y <= HEIGHT:
                            print("Выбран цвет: черный")
                            choiced = True
                            choicedColor = 2

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False

                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                if e.key == p.K_i:
                    playerOne = False
                    playerTwo = False
                    choiced = True
                if e.key == p.K_ESCAPE:
                    running = False
        if choicedColor == 1:
            playerOne = True
            playerTwo = False
        elif choicedColor == 2:
            playerOne = False
            playerTwo = True
        #   ИИ ходы
        if not gameOver and not humanTurn and choiced:
            # if not AIThinking:
            #     AIThinking = True
            #     returnQueue = Queue()
            #     moveFinderProcess = Process(target=SmartMoveFinder.findBestMove, args=(gs, validMoves, returnQueue))
            #     moveFinderProcess.start()
            AIMove = SmartMoveFinder.findBestMove(gs,validMoves)
            # if not moveFinderProcess.is_alive():
            #     AIMove = returnQueue.get()
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
            # AIThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            history = []
            moveHistory = ""
            for i in range(0, len(gs.moveLog)):
                moveHistory = gs.moveLog[i].getChessNotation()
                history.append(moveHistory)
            if len(history)>=8:
                if moveHistory == history[-1] and moveHistory == history[-5] and moveHistory == history[-9]:
                    gs.repeat = True
        if choiced:
            DrawGameState(screen, gs, validMoves, sqSelected,moveLogFont)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Черные объявляют мат')
            else:
                drawText(screen, 'Белые объявляют мат')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Пат')
        elif gs.repeat:
            gameOver = True
            drawText(screen, 'Ничья по трем повторениям')
        else:
            gameOver = False
        clock.tick(FPS)
        p.display.flip()

def DrawChossingColor(screen):
    p.draw.rect(screen, BACKGROUND, (0, 0, WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    screen.blit(IMAGESFORSTART["wQ"], p.Rect(0, 50, 0, 0))
    screen.blit(IMAGESFORSTART["bQ"], p.Rect(WIDTH // 4 * 3 - 30, 50, 0, 0))
#     screen.fill(BACKGROUND)
#     bliting(screen, gs)
#     # DrawBoard(screen)
#     DrawFont(screen)
#     drawBoard(screen)
#     DrawPieces(screen, gs.board)
#     highlightSquares(screen, gs, validMoves, sqSelected)
#     drawMoveLog(screen, gs, moveLogFont)
#     p.draw.rect(screen, BACKGROUND, (0, 0, WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))


def DrawGameState(screen, gs,validMoves,sqSelected,moveLogFont):
    bliting(screen, gs)
    DrawFont(screen)
    drawBoard(screen)
    DrawPieces(screen,gs.board)
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawMoveLog(screen,gs,moveLogFont)


    # screen.blit(IMAGESFORSTART["wQ"], p.Rect(0, 50, 0, 0))
    # screen.blit(IMAGESFORSTART["bQ"], p.Rect(WIDTH // 4 * 3 - 30, 50, 0, 0))
    # pawnPromotionChoice(gs,screen)

def drawBoard(screen):
    global colors
    colors = [LIGHTBLUE,BLUE]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    # p.draw.rect(screen, BACKGROUND, (SQ_SIZE*3, SQ_SIZE * 8 //2,SQ_SIZE*4,SQ_SIZE*2))




def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('pink'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))



# def pawnPromotionChoice(gs,screen):
#     promotionChoices = gs.promotionChoice
#     ChoiceBox = p.Rect(WIDTH/2,HEIGHT/2,SQ_SIZE*4,SQ_SIZE)
#     p.draw.rect(screen,p.Color(BACKGROUND),ChoiceBox)
#     for i in range(len(promotionChoices)):
#         for c in range(len(promotionChoices)):
#             if gs.whiteToMove:
#                 piece = gs.PromotionBoxWhite[c]
#                 if piece != "--":
#                     screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE,SQ_SIZE, SQ_SIZE, SQ_SIZE))







# def DrawBoard(screen):
#
#     is_even_qty = (DIMENSION % 2 == 0)
#     cell_color_index = 1 if (is_even_qty) else 0
#     for y in range(DIMENSION):
#         for x in range(DIMENSION):
#             cell = p.Surface((SQ_SIZE, SQ_SIZE))
#             cell.fill(colors[cell_color_index])
#             fields.blit(cell, (x * SQ_SIZE, y * SQ_SIZE))
#             cell_color_index ^= True
#         cell_color_index = cell_color_index ^ True if (is_even_qty) else cell_color_index

def DrawFont(screen):
    FNT18 = p.font.Font(p.font.get_default_font(), 16)
    for i in range(0, DIMENSION):
        letter = FNT18.render(LTRS[i],1,WHITE)
        number = FNT18.render(str(DIMENSION - i), 1, WHITE)
        n_lines.blit(letter, (
            i * SQ_SIZE + (SQ_SIZE - letter.get_rect().width) // 2,
            (n_lines.get_height() - letter.get_rect().height) // 2
        ))
        n_rows.blit(number, (
            (n_rows.get_width() - letter.get_rect().width) // 2,
            i * SQ_SIZE + (SQ_SIZE - number.get_rect().height) // 2
        ))

def DrawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen,gs,font):
    moveLogRect = p.Rect(WIDTH,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen,p.Color(BACKGROUND), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog),2):
        moveString = str(i//2+1) + ". " + moveLog[i].getChessNotation() + " "
        if i+1 < len(moveLog):
            moveString += moveLog[i+1].getChessNotation() + " "
        moveTexts.append(moveString)


    movesPerRow = 2
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0,len(moveTexts),movesPerRow):
        # text = moveTexts[i]
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color('Black'))
        textLocation = moveLogRect.move(padding,textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def bliting(screen, gs):
    # DrawPieces(fields, gs.board)
    # boardSur.blit(n_rows, (0, n_lines.get_height()))
    boardSur.blit(n_rows, (n_rows.get_width() + fields.get_width(), n_lines.get_height()))
    # boardSur.blit(n_lines, (n_rows.get_width(), 0))
    boardSur.blit(n_lines, (n_rows.get_width(), n_rows.get_width() + fields.get_width()))
    boardSur.blit(fields, (n_rows.get_width(), n_lines.get_height()))
    screen.blit(boardSur, (
        (WIN_SIZE[0] - boardSur.get_width()) // 2,
        (WIN_SIZE[1] - boardSur.get_height()) // 2
    ))


def animateMove(move, screen, board,clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 2
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        DrawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)

        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured],endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(40)


def drawText(screen, text):
    font = p.font.SysFont('Times New Roman',32,True, False)
    textObject = font.render(text,0,p.Color('Black'))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2-50)
    screen.blit(textObject,textLocation)
    textObject = font.render(text, 0, p.Color('Gray'))
    screen.blit(textObject,textLocation.move(2,2))



if __name__ == "__main__":
    main()



