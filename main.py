import pygame
import time
import math


pygame.init()

WIDTH = 800
win = pygame.display.set_mode((600, WIDTH))
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

## Useful text lines
pygame.font.init()
GAME_FONT = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 30)
TIE_TEXT = GAME_FONT.render("TIE", True, (255, 0, 0))
O_WINS = GAME_FONT.render("O wins", True, (255, 0, 0))
X_WINS = GAME_FONT.render("X wins", True, (255, 0, 0))

## load images
X = pygame.image.load("x.jpg")
O = pygame.image.load("o.jpg")
RESET = pygame.image.load("reset.png")

## 3 x 3 board
board = [['']*3, ['']*3, ['']*3]

ai = 'x'
human = 'o'
currentPlayer = human


def draw_grid(win):
    gap = 600 // 3
    for i in range(1, 3):
        pygame.draw.line(win, GREY, (0, i * gap), (600, i * gap), 10)
    for i in range(1, 3):
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, 600), 10)


def check_box(x, y):
    if x in range(0, 200):
        if y in range(0, 200):
            return 0,0
        if y in range(200, 400):
            return 1,0
        if y in range(400, 600):
            return 2,0
    if x in range(200, 400):
        if y in range(0, 200):
            return 0,1
        if y in range(200, 400):
            return 1,1
        if y in range(400, 600):
            return 2,1
    if x in range(400, 600):
        if y in range(0, 200):
            return 0,2
        if y in range(200, 400):
            return 1,2
        if y in range(400, 600):
            return 2,2


def fill_the_rest():
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = "#"


def draw(win, winner):
    win.fill(WHITE)
    draw_grid(win)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'o':
                win.blit(O, (j*200+5, i*200+5))
            elif board[i][j] == 'x':
                win.blit(X, (j*200+5, i*200+5))
    win.blit(RESET, (500, 650))
    if winner == 'tie':
        win.blit(TIE_TEXT, (0,650))
        fill_the_rest()
    elif winner == 'o':
        win.blit(O_WINS, (0,650))
        fill_the_rest()
    elif winner == 'x':
        win.blit(X_WINS, (0,650))
        fill_the_rest()
    
    pygame.display.update()


def check_winner():
    winner = None

    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            winner = board[0][i]
    
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            winner = board[i][0]

    if board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        winner = board[1][1]

    emptySpace = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == '': emptySpace += 1
    
    if winner == None and emptySpace == 0:
        return 'tie'
    return winner


def bestMove():
    bestScore = -math.inf
    move = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > bestScore:
                    bestScore = score
                    move = [i, j]
    try:
        board[move[0]][move[1]] = ai
    except:
        pass


scores = {
    'x' : 10,
    'o' : -10,
    'tie' : 0
}

def minimax(board, depth, isMaximizing):
    result = check_winner()
    if result == 'tie' or result == 'x' or result == 'o':
        return scores[result]

    if isMaximizing:
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = ai
                    score = minimax(board, depth+1, False)
                    board[i][j] = ''
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = human
                    score = minimax(board, depth+1, True)
                    board[i][j] = ''
                    bestScore = min(score, bestScore)
        return bestScore



run = True
winner = None
while run:
    if currentPlayer == ai:
        bestMove()
        winner = check_winner()
        currentPlayer = human
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x in range(500, 550) and y in range(650, 700):
                board = [['']*3, ['']*3, ['']*3]
                winner = None
            try:
                i,j = check_box(x, y)
                if i in range(3) and j in range(3) and board[i][j] == '':
                    board[i][j] = currentPlayer
                    currentPlayer = human if currentPlayer == ai else ai
                winner = check_winner()
                if winner == 'tie':
                    win.blit(TIE_TEXT, (0,0))
                elif winner == 'o':
                    win.blit(O_WINS, (0,0))
                elif winner == 'x':
                    win.blit(X_WINS, (0,0))
            except:
                print("out side the box")
            
    draw(win, winner)
pygame.quit()