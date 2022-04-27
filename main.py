import pygame
from pygame.draw import *
import time
import random
import ctypes

pygame.init()

WIDTH = 900
HEIGHT = 750
VWIDTH = 740
VHEIGHT = 740
DIMENSIONS = (WIDTH, HEIGHT)
NODESIZE = 20

BOARD_WIDTH = 37
BOARD_HEIGHT = 37

RANDOM_CONST = 5

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = ( 39, 249,  48)
RED    = (250,  37,  26)
GREY   = ( 51,  51,  51)
LGREY  = (100, 100, 100)
BLUE   = ( 66,  98, 249)
YELLOW = (255, 255,   0)

window = pygame.display.set_mode(DIMENSIONS)
window.fill(BLACK)

gameFont = pygame.font.Font('freesansbold.ttf', 32)
text = gameFont.render('', True, WHITE, GREY)
startFont = gameFont.render('Start', True, BLACK, LGREY)
startRect = text.get_rect()
startRect.topleft = (750, 25)

resetFont = gameFont.render('Reset', True, BLACK, LGREY)
resetRect = text.get_rect()
resetRect.topleft = (750, 70)

randomFont = gameFont.render('Random', True, BLACK, LGREY)
randomRect = text.get_rect()
randomRect.topleft = (750, 115)

def showBoard(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if not ((j, i) == start or (j, i) == end):
                rect(window, GREY if cell == 0 else WHITE, (j * NODESIZE, i * NODESIZE, NODESIZE - 1, NODESIZE - 1))
    pygame.display.update()

def showPath(path):
    for i in path:
        if not (i == start or i == end):
            rect(window, YELLOW, (i[1] * NODESIZE, i[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
            pygame.display.update()
            time.sleep(0.02)


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0

    def __eq__(self, other):
        return self.position == other.position

def h(start, end):
    return (((start.position[0] - end.position[0]) ** 2) + ((start.position[1] - end.position[1]) ** 2))**0.5
    
def A_star(board, start, end):
    startnode = Node(None, start)
    startnode.gcost =0
    startnode.hcost =0
    startnode.fcost = 0
    endnode = Node(None, end)
    startnode.gcost =0
    startnode.hcost =0
    startnode.fcost = 0

    openlist = []
    closedlist = []

    openlist.append(startnode)
    while len(openlist) > 0:
        
        currentnode = openlist[0]
        currentpos = 0
        for pos, obj in enumerate(openlist):
            if obj.fcost < currentnode.fcost:
                
                currentnode = obj
                currentpos= pos
        openlist.pop(currentpos)
        closedlist.append(currentnode)
        #print(currentnode.position)
        if not (currentnode.position == start or currentnode.position == end):
            rect(window, BLUE, (currentnode.position[1] * NODESIZE, currentnode.position[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
            pygame.display.update()
            #time.sleep(0.01)
        else:
            rect(window, RED, (start[1] * NODESIZE, start[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
            rect(window, GREEN, (end[1] * NODESIZE, end[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
            pygame.display.update()
        
        if currentnode == endnode:
            print('path found')
          
            path = []
            tempcurrent=currentnode
            while tempcurrent is not None:
                path.append(tempcurrent.position)
                tempcurrent = tempcurrent.parent
            return path[::-1]


        children = []
        for newpos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            
            nodepos = (currentnode.position[0] + newpos[0], currentnode.position[1] + newpos[1])
            
            if nodepos[0] > (BOARD_WIDTH) or nodepos[0] < 0 or nodepos[1] > (BOARD_HEIGHT) or nodepos[1] < 0:               
                continue

            if nodepos[0] > (len(board) - 1) or nodepos[0] < 0 or nodepos[1] > (len(board[len(board)-1]) -1) or nodepos[1] < 0:
                continue
               
            if board[nodepos[0]][nodepos[1]] != 0:
                continue

            if newpos == (-1, -1):
                if board[nodepos[0] + 1][nodepos[1]] != 0 and board[nodepos[0]][nodepos[1] + 1] != 0:
                    continue
            if newpos == (-1, 1):
                if board[nodepos[0]][nodepos[1] - 1] != 0 and board[nodepos[0] + 1][nodepos[1]] != 0:
                    continue
            if newpos == (1, -1):
                if board[nodepos[0] - 1][nodepos[1]] != 0 and board[nodepos[0]][nodepos[1] + 1] != 0:
                    continue
            if newpos == (1, 1):
                if board[nodepos[0] - 1][nodepos[1]] != 0 and board[nodepos[0]][nodepos[1] - 1] != 0:
                    continue
            
            newnode = Node(currentnode, nodepos)
            children.append(newnode)

        for child in children:
            if len([closedchild for closedchild in closedlist if closedchild.position == child.position]) >0:
                continue

            child.gcost = currentnode.gcost + h(child,currentnode)
            child.hcost = h(child,endnode)
            child.fcost = child.gcost + child.hcost


            if len([opennode for opennode in openlist if child.position == opennode.position and child.fcost >= opennode.fcost]) > 0:
                continue
            openlist.append(child)

       
board = [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]

start = (0, 0)
end = (BOARD_WIDTH - 1, BOARD_HEIGHT - 1)
board[end[0]][end[1]] = 0

rect(window, RED, (start[1] * NODESIZE, start[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
rect(window, GREEN, (end[1] * NODESIZE, end[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
pygame.display.update()

run = True

dragging = False
startDrag = False
endDrag = False

window.blit(startFont, startRect)
window.blit(resetFont, resetRect)
window.blit(randomFont, randomRect)
pygame.display.update()

showBoard(board)

while run:

    pygame.time.delay(160)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            if (pygame.mouse.get_pos()[1] // NODESIZE, pygame.mouse.get_pos()[0] // NODESIZE) == start:
                startDrag = True
            elif (pygame.mouse.get_pos()[1] // NODESIZE, pygame.mouse.get_pos()[0] // NODESIZE) == end:
                endDrag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            startDrag = False
            endDrag = False

    if dragging:
        currentX, currentY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        if currentX < VWIDTH and currentY < VHEIGHT:
            if startDrag:
                board[start[0]][start[1]] = 0
                rect(window, GREY, (start[1] * NODESIZE, start[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                start = (currentY // NODESIZE, currentX // NODESIZE)
                rect(window, RED, (start[1] * NODESIZE, start[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                pygame.display.update()
              
            elif endDrag:
                board[end[0]][end[1]] = 0
                rect(window, GREY, (end[1] * NODESIZE, end[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                end = (currentY // NODESIZE, currentX // NODESIZE)
                rect(window, GREEN, (end[1] * NODESIZE, end[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                pygame.display.update()

            if not (startDrag or endDrag):  
                if board[currentY // NODESIZE][currentX // NODESIZE] == 0:
                    board[currentY // NODESIZE][currentX // NODESIZE] = 1
                    rect(window,  WHITE, (currentX // NODESIZE * NODESIZE, currentY // NODESIZE * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                    pygame.display.update()

                    
                elif board[currentY // NODESIZE][currentX // NODESIZE] == 1:
                    board[currentY // NODESIZE][currentX // NODESIZE] = 0
                    rect(window,  GREY, (currentX // NODESIZE * NODESIZE, currentY // NODESIZE * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                    pygame.display.update()
        else:
            if currentX >= 750 and currentX <= 820 and currentY >= 25 and currentY <= 60:
                break
            elif currentX >= 750 and currentX <= 820 and currentY >= 70 and currentY <= 105:
                board = [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]
                start = (0, 0)
                end = (BOARD_WIDTH - 1, BOARD_HEIGHT - 1)
                rect(window, RED, (start[1] * NODESIZE, start[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                rect(window, GREEN, (end[1] * NODESIZE, end[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                showBoard(board)
            elif currentX >= 750 and currentX <= 820 and currentY >= 115 and currentY <= 150:
                board = [[random.randint(0, 1) for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]
                board[0][0] = 0
                board[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = 0
                start = (0, 0)
                end = (BOARD_WIDTH - 1, BOARD_HEIGHT - 1)
                rect(window, RED, (start[1] * NODESIZE, start[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                rect(window, GREEN, (end[1] * NODESIZE, end[0] * NODESIZE, NODESIZE - 1, NODESIZE - 1))
                showBoard(board)


showBoard(board)
path = A_star(board,start,end)

if type(path) == type(None):
    print("No Path Found :(")
    if ctypes.windll.user32.MessageBoxW(0, "No Path Found", ":(", 5) == 4:
        exec(open('main.py').read())
    quit()

showPath(path)
if ctypes.windll.user32.MessageBoxW(0, "Path Found!", ":)", 5) == 4:
    exec(open('main.py').read())
print(path)
