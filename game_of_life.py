
    
import pygame, math, random,copy
pygame.init()

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

PIXEL_SIZE = 5

#Update ever UPDATETIME ms
UPDATETIME = 1
TARGET_FPS = 100


#For a space that is 'populated':
#    Each cell with one or no neighbors dies, as if by loneliness. 
#    Each cell with four or more neighbors dies, as if by overpopulation. 
#    Each cell with two or three neighbors survives. 
#For a space that is 'empty' or 'unpopulated'
#    Each cell with three neighbors becomes populated. 

class Grid():
    
    def __init__(self,*args, **kwargs):
        self.grid = [[False for i in range(WINDOW_HEIGHT/PIXEL_SIZE)] for i in range(WINDOW_WIDTH/PIXEL_SIZE)]

    def setCell(self,x,y,status):
        self.grid[x][y] = status
        
    def getCell(self,x,y):
        return self.grid[x][y]
     
    def countNeighbours(self,x,y):
        try:
            #Could do this in some really fancy spangled way but so much easier to read like this
            count = 0
            if self.getCell(x-1,y-1): count += 1
            if self.getCell(x,y-1): count += 1
            if self.getCell(x+1,y-1): count += 1
            if self.getCell(x-1,y): count += 1
            if self.getCell(x+1,y): count += 1
            if self.getCell(x-1,y+1): count += 1
            if self.getCell(x,y+1): count += 1
            if self.getCell(x+1,y+1): count += 1
        except:
            return 0

        return count

class Debug_text():
    def __init__(self,screen,clock,active_cells = 0, *args, **kwargs):
        #self.points = kwargs.pop('points')
        self.screen = screen
        self.clock = clock
        self.active = active_cells
        self.font = pygame.font.SysFont("Monospaced", 20)
    
    def print_text(self):
        label_active = self.font.render("# Active Cells: " + str(self.active), 1, (255,255,255))
        label_frameRate = self.font.render("FPS: " + str(self.clock.get_fps()), 1, (255,255,255))
        self.screen.blit(label_active, (10, 10))
        self.screen.blit(label_frameRate, (10, 20))

    def update(self,*args, **kwargs):
        self.screen = kwargs.get("screen",self.screen)
        self.clock = kwargs.get("clock",self.clock)
        self.active = kwargs.get("active",self.active)
 
def drawSquare(background, x,y):
    #colour = random.randint(0,255),random.randint(0,255),random.randint(0,255)
    colour=(0,255,0)
    pygame.draw.rect(background, colour, (x*PIXEL_SIZE,y*PIXEL_SIZE,PIXEL_SIZE,PIXEL_SIZE))       

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    clock = pygame.time.Clock()

    keepGoing = True
    mousebuttondown = False
    
    lastrun = pygame.time.get_ticks()
    grid = Grid()  
    debug = Debug_text(screen, clock)  

    #Create the orginal grid patteren randomly
    for x in xrange(0,WINDOW_WIDTH/PIXEL_SIZE):
            for y in xrange(0, WINDOW_HEIGHT/PIXEL_SIZE):
                if random.randint(0,10)==1:
                    grid.setCell(x, y, True)
                    drawSquare(background,x,y)

    screen.blit(background, (0, 0)) 
    pygame.display.flip()


    #program loop
    while keepGoing:
        ##GO MAD!!
        clock.tick(TARGET_FPS)
        newgrid = Grid()

        ##Loops though creating new grid based on last grid and game of life rules
        ##Limit the number of time it updates, slows it down a bit. Takes the limit off the fps
        if pygame.time.get_ticks() - lastrun > UPDATETIME:
            number_active_cells = 0
            background.fill((0, 0, 0))
            for x in xrange(0,WINDOW_WIDTH/PIXEL_SIZE):
                for y in xrange(0, WINDOW_HEIGHT/PIXEL_SIZE):
                    if grid.getCell(x,y):
                        if grid.countNeighbours(x,y) < 2:
                            newgrid.setCell(x,y,False)
                        elif grid.countNeighbours(x,y) <= 3:
                            newgrid.setCell(x,y,True)
                            number_active_cells += 1
                            drawSquare(background,x,y)
                        elif grid.countNeighbours(x,y) >= 4:
                            newgrid.setCell(x,y,False)
                    else:
                        if grid.countNeighbours(x,y) == 3:
                            newgrid.setCell(x,y,True)
                            number_active_cells += 1
                            drawSquare(background,x,y)
            lastrun = pygame.time.get_ticks() 
        else:
            newgrid = grid
            
        debug.update(active = number_active_cells)
        
 
        ##Events, manly looking for mouse click. Adds points when mouse is held down
        mousebuttondown = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown = True             
                while mousebuttondown:
                    #print pygame.mouse.get_pos()    
                    newgrid.setCell(pygame.mouse.get_pos()[0]/PIXEL_SIZE,pygame.mouse.get_pos()[1]/PIXEL_SIZE,True)
                    drawSquare(background,pygame.mouse.get_pos()[0]/PIXEL_SIZE,pygame.mouse.get_pos()[1]/PIXEL_SIZE)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            mousebuttondown = False
                    
                    screen.blit(background, (0, 0)) 
                    pygame.display.flip()


        #Draws the new grid
        grid = newgrid       

        #updates screen
        
        screen.blit(background, (0, 0)) 
        debug.update(active = number_active_cells)
        debug.print_text()
        pygame.display.flip()
       
if __name__ == "__main__":
    main()



 

