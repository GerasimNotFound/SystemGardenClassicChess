import pygame as p
from Chess import ChessEngine
p.display.set_caption('Шахматы')
WIN_SIZE = 630, 630
SIZE = 600
DIMENSION = 8
SQ_SIZE = SIZE // DIMENSION
FPS = 40
IMAGES = {}
LIGHTBLUE = (132,196,192)
BLUE = (0,86,143)
WHITE = (255,255,255)
BACKGROUND = (230,96,114)
LTRS = 'ABCDEFGH'
colors = [BLUE, LIGHTBLUE]
screen = p.display.set_mode(WIN_SIZE)
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

def load_Images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))



def main():
    p.init()
    screen.fill(BACKGROUND)
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    load_Images()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: # Реализация ходов через клики
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): # Пользователь нажал на одну и ту же клетку 2 раза
                    sqSelected = () # отмена выбора
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #После второго клика
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            # animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        DrawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(FPS)
        p.display.flip()


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

def DrawGameState(screen, gs,validMoves,sqSelected):
    bliting(screen, gs)
    drawBoard(screen)
    highlightSquares(screen,gs,validMoves,sqSelected)
    DrawFont(screen)


def drawBoard(screen):
    global colors
    is_even_qty = (DIMENSION % 2 == 0)
    cell_color_index = 1 if (is_even_qty) else 0
    for y in range(DIMENSION):
        for x in range(DIMENSION):
            cell = p.Surface((SQ_SIZE, SQ_SIZE))
            cell.fill(colors[cell_color_index])
            fields.blit(cell, (x * SQ_SIZE, y * SQ_SIZE))
            cell_color_index ^= True
        cell_color_index = cell_color_index ^ True if (is_even_qty) else cell_color_index

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

def DrawPieces(fields, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                fields.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def bliting(screen, gs):
    DrawPieces(fields, gs.board)
    boardSur.blit(n_rows, (0, n_lines.get_height()))
    boardSur.blit(n_rows, (n_rows.get_width() + fields.get_width(), n_lines.get_height()))
    boardSur.blit(n_lines, (n_rows.get_width(), 0))
    boardSur.blit(n_lines, (n_rows.get_width(), n_rows.get_width() + fields.get_width()))
    boardSur.blit(fields, (n_rows.get_width(), n_lines.get_height()))
    screen.blit(boardSur, (
        (WIN_SIZE[0] - boardSur.get_width()) // 2,
        (WIN_SIZE[1] - boardSur.get_height()) // 2
    ))

# def animateMove(move, screen, board,clock):
#     global colors
#     dR = move.endRow - move.startRow
#     dC = move.endCol - move.startCol
#     framesPerSquare = 2
#     frameCount = (abs(dR) + abs(dC)) * framesPerSquare
#     for frame in range(frameCount + 1):
#         r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
#         drawBoard(screen)
#         DrawPieces(screen, board)
#
#         color = colors[(move.endRow + move.endCol) % 2]
#         endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
#         p.draw.rect(screen,color,endSquare)
#
#         if move.pieceCaptured != '--':
#             screen.blit(IMAGES[move.pieceCaptured],endSquare)
#
#         screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
#         p.display.flip()
#         clock.tick(40)




if __name__ == "__main__":
    main()



