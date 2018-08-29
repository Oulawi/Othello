import pygame
import socket
import pickle

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("127.0.0.1", 5000))

pygame.init()
pygame.mixer.quit()
pygame.display.set_caption("Othello (whites)")

grid = []
def init_grid():
    for i in range (0, 8, 1):
        grid.append([0, 0, 0, 0, 0, 0, 0, 0])

init_grid()

turnCount = 1
grid[3][3] = 2
grid[3][4] = 1
grid[4][3] = 1
grid[4][4] = 2

#Essential functions for the game
def findMouseLoc():
    def findMouseX():
        coordinates = pygame.mouse.get_pos()
        x = coordinates[0]
        for i in range(1, 10, 1):
            if x - (120*i + 2*i) <= 0:
                return(i-1)
    def findMouseY():
        coordinates = pygame.mouse.get_pos()
        y = coordinates[1]
        for i in range(1, 10, 1):
            if y - (120*i + 2*i) <= 0:
                return(i-1)
    return([findMouseX(), findMouseY()])  

clock = pygame.time.Clock()
tickrate = 20
screen = pygame.display.set_mode([978, 978])
done = False

screen.fill([16, 112, 16])
    
for i in range(0, 8, 1):
    pygame.draw.rect(screen, [0,0,0], pygame.Rect(120 * i + 2 * i, 0, 2, 978))
    pygame.draw.rect(screen, [0,0,0], pygame.Rect(0, 120 * i + 2 * i, 978, 2))

for i in range(0, 8, 1):
    for u in range(0, 8, 1):
        if grid[i][u] == 1:
            pygame.draw.circle(screen, [0, 0, 0], [120*i + 2*i + 60, 120*u + 2*u + 60], 50)
        elif grid[i][u] == 2:
            pygame.draw.circle(screen, [255, 255, 255], [120*i + 2*i + 60, 120*u + 2*u + 60], 50)
pygame.display.update()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #Game logic
    #Black turn
    playerMove = None
    pressed = pygame.key.get_pressed()
    if turnCount % 2 == 1:
        packetIn = connection.recv(4096)
        grid = pickle.loads(packetIn)
        turnCount += 1
        

    #White turn        
    elif turnCount % 2 == 0:
        if pygame.mouse.get_pressed()[0] == 1 and grid[findMouseLoc()[0]][findMouseLoc()[1]] != 1 and grid[findMouseLoc()[0]][findMouseLoc()[1]] != 2:
            playerMove = findMouseLoc()
            lines = 0
            #Check to the right
            for i in range(playerMove[0] + 1, 8, 1):
                if grid[i][playerMove[1]] == 2 and  i != playerMove[0] + 1:
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[0], i, 1):
                        grid[u][playerMove[1]] = 2
                    lines += 1
                    break
                elif grid[i][playerMove[1]] == 1:
                    None
                else:
                    break
            #Check to the left
            for i in range(playerMove[0] - 1, 0, -1):
                if grid[i][playerMove[1]] == 2 and  i != playerMove[0] - 1:
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[0], i, -1):
                        grid[u][playerMove[1]] = 2
                    lines += 1
                    break
                elif grid[i][playerMove[1]] == 1:
                    None
                else:
                    break
            #Check to the bottom
            for i in range(playerMove[1] + 1, 8, 1):
                if grid[playerMove[0]][i] == 2 and  i != playerMove[1] + 1:
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[1], i, 1):
                        grid[playerMove[0]][u] = 2
                    lines += 1
                    break
                elif grid[playerMove[0]][i] == 1:
                    None
                else:
                    break
            #Check to the top
            for i in range(playerMove[1] - 1, 0, -1):
                if grid[playerMove[0]][i] == 2 and  i != playerMove[1] - 1:
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[1], i, -1):
                        grid[playerMove[0]][u] = 2
                    lines += 1
                    break
                elif grid[playerMove[0]][i] == 1:
                    None
                else:
                    break
            #Check to the bottom right
            y = playerMove[1] + 1
            for i in range(playerMove[0] + 1, 8, 1):
                if y == 8:
                    break
                elif grid[i][y] == 2 and i != playerMove[0] + 1:
                    d = playerMove[1] + 1
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[0] + 1, i + 1, 1):
                        grid[u][d] = 2
                        d += 1
                    lines += 1
                    break
                elif grid[i][y] == 1:                        
                    y += 1
                else:
                    break
            #Check to the top right
            y = playerMove[1] - 1
            for i in range(playerMove[0] + 1, 8, 1):
                if y < 0:
                    break
                elif grid[i][y] == 2 and i != playerMove[0] + 1:
                    d = playerMove[1] - 1
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[0] + 1, i + 1, 1):
                        grid[u][d] = 2
                        d -= 1
                    lines += 1
                    break
                elif grid[i][y] == 1:                        
                    y -= 1
                else:
                    break
            #Check to the bottom left
            y = playerMove[1] + 1
            for i in range(playerMove[0] - 1, 0, -1):
                if y == 8:
                    break
                elif grid[i][y] == 2 and i != playerMove[0] - 1:
                    d = playerMove[1] + 1
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[0] - 1, i - 1, -1):
                        grid[u][d] = 2
                        d += 1
                    lines += 1
                    break
                elif grid[i][y] == 1:                        
                    y += 1
                else:
                    break
            #Check to the top left
            y = playerMove[1] - 1
            for i in range(playerMove[0] - 1, 0, -1):
                if y < 0:
                    break
                elif grid[i][y] == 2 and i != playerMove[0] - 1:
                    d = playerMove[1] - 1
                    grid[playerMove[0]][playerMove[1]] = 2
                    for u in range(playerMove[0] - 1, i - 1, -1):
                        grid[u][d] = 2
                        d -= 1
                    lines += 1
                    break
                elif grid[i][y] == 1:                        
                    y -= 1
                else:
                    break


            if lines == 0:
                print("Invalid move")
            elif pressed[pygame.K_f]:
                turnCount += 1
                packetOut = pickle.dumps(grid)
                connection.send(packetOut)
            else:
                turnCount += 1
                packetOut = pickle.dumps(grid)
                connection.send(packetOut)


    


    #Drawing
    screen.fill([16, 112, 16])
    
    for i in range(0, 8, 1):
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(120 * i + 2 * i, 0, 2, 978))
        pygame.draw.rect(screen, [0,0,0], pygame.Rect(0, 120 * i + 2 * i, 978, 2))

    for i in range(0, 8, 1):
        for u in range(0, 8, 1):
            if grid[i][u] == 1:
                pygame.draw.circle(screen, [0, 0, 0], [120*i + 2*i + 60, 120*u + 2*u + 60], 50)
            elif grid[i][u] == 2:
                pygame.draw.circle(screen, [255, 255, 255], [120*i + 2*i + 60, 120*u + 2*u + 60], 50)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(tickrate)

pygame.quit()