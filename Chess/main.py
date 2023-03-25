import pygame as p
from Chess import ChessEngine
p.display.set_caption('Шахматы')
WIN_SIZE = 800, 800
SIZE = 600
DIMENSION = 8
SQ_SIZE = SIZE // DIMENSION
FPS = 15
IMAGES = {}
LIGHTBLUE = (132,196,192)
BLUE = (0,86,143)
BACKGROUND = (230,96,114)

def load_Images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))



def main():
    p.init()
    screen = p.display.set_mode(WIN_SIZE)
    clock = p.time.Clock()
    screen.fill(p.Color(255,255,255))
    gs = ChessEngine.GameState()
    load_Images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        DrawGameState(screen, gs)
        clock.tick(FPS)
        p.display.flip()

def DrawGameState(screen, gs):
    DrawBoard(screen)
    DrawPieces(screen, gs.board)


def DrawBoard(screen):
    colors = [p.Color(LIGHTBLUE), p.Color(BLUE)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE ))

def DrawFont(screen):
    pass

def DrawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c* SQ_SIZE, r* SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()



