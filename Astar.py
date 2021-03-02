
from collections import defaultdict
import pygame,sys,math
from pygame.locals import *


# GLOBAL VARS

#screen width/height
s_width = 1728
s_height = 972



class node:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        else:
            return False
    def __hash__(self):
        return hash((self.x,self.y))

    def __str__(self):
        return "({},{})".format(self.x,self.y)


# what directions can you move [x,y]
dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]


def neighbours(cur,walls, xmax,ymax):
    ret = []
    for d in dirs:
        n = node(cur.x+d[0],cur.y+d[1])
        if (0 <= n.x < xmax and 0 <= n.y < ymax) and walls[n.y][n.x] == 0:
            ret.append(n)
    return ret


def reconstruct_path(came_from, current):
    path = []
    while current in came_from.keys():
        path.insert(0,current)
        current = came_from[current]
    return path


def d(c,n):
    if c.x-n.x and c.y-n.y:
        return math.sqrt(2)
    else:
        return 1

def draw_grid(surface,row,col):
    for i in range(col+1):
        pygame.draw.line(surface, (128, 128, 128), (0, i * block_size),
                         (width*block_size,i * block_size))  # horizontal lines
        for j in range(row+1):
            pygame.draw.line(surface, (128, 128, 128), (j * block_size, 0),
                             (j * block_size, height*block_size))  # vertical lines

def draw_walls(win, walls, xmax, ymax):
    for i in range(ymax):
        for j in range(xmax):
            if walls[i][j]:
                pygame.draw.rect(win,(255,255,255),(j * block_size,i * block_size, block_size, block_size))
def draw_seen(surface,seen,start,finish):
    red = h(start,finish)
    yellow = red/2
    for s in seen:
        dist = h(s,finish)
        if dist>red:
            colour = (255,0,0)
        elif dist>yellow:
            shade = (red-dist)/yellow*255
            colour = (255,shade,0)
        else:
            shade = dist/yellow*255
            colour = (shade,255,0)
        pygame.draw.rect(surface,colour,(s.x*block_size,s.y*block_size,block_size,block_size))
    pygame.draw.rect(surface, (255,0,0), (start.x * block_size,start.y * block_size, block_size, block_size))
    pygame.draw.rect(surface, (0,255,0), (finish.x * block_size,+ finish.y * block_size, block_size, block_size))


def Astar(win, start, finish,xmax,ymax):

    clock = pygame.time.Clock()
    seen = [start]
    came_from = {}

    gscore = defaultdict(lambda: float('inf'))
    gscore[start] = 0

    fscore = defaultdict(lambda: float('inf'))
    fscore[start] = h(start,finish)

    walls = [[0 for x in range(xmax)] for y in range(ymax)]

    drawing = False
    last_pos = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    running = False
                    break
            elif event.type == MOUSEMOTION:
                if drawing:
                    mouse_position = pygame.mouse.get_pos()

                    #drawing line between last position and current
                    if last_pos is not None:
                        p0 = [last_pos[0] // block_size, last_pos[1] // block_size]
                        p1 = [mouse_position[0] // block_size,mouse_position[1]// block_size]
                        for x in range(abs(p0[0]-p1[0])+1):
                            for y in range(abs(p0[1]-p1[1])+1):
                                p = [min(p0[0], p1[0]) + x, min(p0[1], p1[1]) + y]
                                if p[0] < xmax and p[1] < ymax:
                                    pygame.draw.rect(win, (255,255,255), (p[0] * block_size, p[1] * block_size, block_size, block_size))
                                    walls[p[1]][p[0]] = 1
                        pygame.display.update()
                    last_pos = mouse_position
            elif event.type == MOUSEBUTTONUP:
                last_pos = None
                drawing = False
            elif event.type == MOUSEBUTTONDOWN:
                drawing = True
    win.fill((0,0,0))
    draw_grid(win, xmax, ymax)
    draw_walls(win, walls, xmax, ymax)
    pygame.display.update()

    while seen:
        pygame.event.pump()
        draw_seen(win,seen,start,finish)
        current = min(seen,key = lambda x: fscore[x])
        clock.tick()
        if current == finish:
            path = reconstruct_path(came_from,current)
            n = start
            for p in path:
                pygame.draw.line(win, (255, 255, 255), (n.x*block_size + block_size / 2, n.y*block_size + block_size / 2),
                                 (p.x*block_size + block_size / 2, p.y*block_size + block_size / 2),2)
                n = p

            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        pygame.quit()
                        quit()
            return path

        seen.remove(current)
        for n in neighbours(current,walls,xmax,ymax):
            tentative = gscore[current] + d(current,n)
            if tentative < gscore[n]:
                came_from[n] = current
                gscore[n] = tentative
                fscore[n] = gscore[n] + h(n,finish)
                if n not in seen:
                    seen.append(n)

        pygame.display.update()


def h(node,goal):
    dx = abs(node.x - goal.x)
    dy = abs(node.y - goal.y)
    return math.sqrt(dx**2+dy**2)



#ask for xmax,ymax,start and finish
width = input("Enter the width of the grid (10 <= width <= 200): ")
while True:
    try:
        width = int(width)
        if 10 <= width <= 200:
            break
        else:
            width = input("Enter the width of the grid (10 <= width <= 200): ")
    except:
        width = input("Please enter an integer: ")

height = input("Enter the height of the grid (10 <= height <= 100): ")
while True:
    try:
        height = int(height)
        if 10 <= height <= 100:
            break
        else:
            height = input("Enter the height of the grid (10 <= height <= 100): ")
    except:
        height = input("Please enter an integer: ")

block_size = min(math.floor(s_width/width),math.floor(s_height/height))



start = node(0,0)
finish = node(50,50)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Astar')


draw_grid(win,width,height)
pygame.display.update()
mouse_position = (0, 0)
pygame.init()
myfont = pygame.font.SysFont('Arial', 30)
text_surface = myfont.render("Click where you'd like the start to be",False,(255,255,255))
win.blit(text_surface,(100,100))
pygame.display.update()
start_selected = False
end_selected = False
while not (start_selected and end_selected):
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            pos = [mouse_position[0] // block_size, mouse_position[1]// block_size]
            if start_selected:
                finish = node(pos[0],pos[1])
                end_selected = True
                win.fill((0, 0, 0))
                draw_grid(win, width, height)
                pygame.draw.rect(win, (255, 0, 0), (start.x * block_size, start.y * block_size, block_size, block_size))
                pygame.draw.rect(win, (0, 255, 0), (finish.x * block_size, finish.y * block_size, block_size, block_size))
                text_surface = myfont.render("Draw a maze by clicking and dragging and hit enter when you're done", False, (255, 255, 255))
                win.blit(text_surface, (100, 100))
                pygame.display.update()
            else:
                start = node(pos[0],pos[1])
                start_selected = True
                win.fill((0,0,0))
                draw_grid(win, width, height)
                pygame.draw.rect(win, (255,0,0), (start.x * block_size,start.y * block_size, block_size, block_size))
                text_surface = myfont.render("Click where you'd like the end to be", False, (255, 255, 255))
                win.blit(text_surface, (100, 100))
                pygame.display.update()

path = Astar(win,start,finish,width,height)