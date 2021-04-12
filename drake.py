import pygame
import pygame.examples.scaletest
import random
from pygame import mixer

mixer.init()
  
# Loading the song
sound = pygame.mixer.Sound('apple.wav')
mixer.music.load("song.mp3")
  
# Setting the volume
mixer.music.set_volume(0.05)
  
# Start playing the song
mixer.music.play()

pygame.init()
#RGB values
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
display_width = 800
display_height = 600
#defining the snake
image = pygame.image.load('./Head-snake.png')
aimg = pygame.image.load('./Food-snake.png')
block_size = 24
#not a good idea to change the speed since it has to be equal with block_size, else the collision
#of snake and apple will not match
speed = 13
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Drake!')
fps = 30
direction = 'right'
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,25)
smallfont = pygame.font.SysFont('comicsansms',25)
mediumfont = pygame.font.SysFont('comicsansms',50)
largefont = pygame.font.SysFont('comicsansms',150)
icon = pygame.image.load('./Food-snake.png')
pygame.display.set_icon(icon)
with open("highscore.txt","r") as f:
    highscore = f.read()
 #drawing the snake
def snake(block_size, snakeList ):
    if direction == 'right':
        head = pygame.transform.rotate(image,270)
    if direction == 'left':
        head = pygame.transform.rotate(image,90)
    if direction == 'up':
        head = image
    if direction == 'down':
        head = pygame.transform.rotate(image,180)

    gameDisplay.blit(head,(snakeList[-1][0], snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay,white,(XnY[0],XnY[1],block_size ,block_size), width= 1, border_radius=50)

def text_objects(msg,color,size):
    if size == 'small':
        textSurface = smallfont.render(msg,True,color)
        return textSurface, textSurface.get_rect()
    elif size == 'medium':
        textSurface = mediumfont.render(msg,True,color)
        return textSurface, textSurface.get_rect()
    elif size == 'large':
        textSurface = largefont.render(msg,True,color)
        return textSurface, textSurface.get_rect()

#function to display textmessages on screen
def message_to_screen(msg,color,x_displace = 0, y_displace = 0, size='small'):
    textSurf,textRect = text_objects(msg,color,size)
    # => get_rect().center returns a rectangle covering the surface, in this case it's the text ones
    textRect.center = (display_width/2) + x_displace , (display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def randAppleGen():
    randAppleX = round(random.randrange(0,display_width-block_size)/10)*10
    randAppleY = round(random.randrange(0,display_height-block_size)/10)*10
    return randAppleX, randAppleY

def game_intro():
    intro = True

    while intro:
        with open("highscore.txt","r") as f:
            highscore = f.read()
        gameDisplay.fill(black)
        message_to_screen('Welcome!', white , y_displace= -100, size='large')
        message_to_screen('Press any Key to play Drake!',white, y_displace = 30, size='medium')
        message_to_screen(('Highscore = '+ str(highscore)),white, y_displace = 130, size='medium')
        message_to_screen('(P = Pause E =  Pause Music  R = Resume Music)',white,y_displace = 230,x_displace = 0, size='small')


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                intro = False

def pause():
    paused = True
 #   message_to_screen('Pause',black,y_displace = -100,size = 'large')
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
    pygame.display.update()
    clock.tick(3)

def gameLoop():

    game_intro()
    global direction
    direction = 'right'
    #current position of t he snake
    lead_x = display_width/2
    lead_y = display_height/2
    #current course of the snake
    lead_x_change = 10
    lead_y_change = 0
    #structure of the snake, List contains  X x Y tuple
    snakeList = []
    snakeLength = 1
    appleThickness = 30
    #generating random X Y coordinates for the apple
    randAppleX, randAppleY = randAppleGen()
    gameExit = False
    gameOver = False
    #gameloop starts here
    while not gameExit:
        #menu on gameover
        while gameOver == True:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            gameDisplay.fill(black)
            message_to_screen('Game Over',white,0,-50,size='large')
            message_to_screen('Press Q to quit and C to continue',white,0,50,size='small')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                gameOver = False
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -speed
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = speed
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    lead_y_change = -speed
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    lead_y_change = speed
                    lead_x_change = 0
                    direction ='down'
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_ESCAPE:
                    gameExit = True
                
                if event.key == pygame.K_e:
                # Pausing the music
                    mixer.music.pause()     
                elif event.key == pygame.K_r:
                # Resuming the music
                    mixer.music.unpause()
            
        #checking if snake is out of window
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
        #updating current position of the snake
        lead_x += lead_x_change
        lead_y += lead_y_change
        #drawing the background screen
        gameDisplay.fill(black)
        with open("highscore.txt","r") as f:
            highscore = f.read()
        score = int(snakeLength-1)
        if int(score) >int(highscore):
            highscore = score
        message_to_screen(('Score: ' + str(score) ),white,-350,-270)
        message_to_screen(('Highscore: ' + str(highscore) ),white,300,-270)
        #drawing the apple
        gameDisplay.blit(aimg,(randAppleX,randAppleY))
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
           del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size,snakeList)
        pygame.display.update()

        #behavior if snake runs over apple
        if lead_x + block_size > randAppleX and lead_x < randAppleX + appleThickness:
            if lead_y + block_size > randAppleY and lead_y < randAppleY + appleThickness:
               # pygame.draw.rect(gameDisplay,(255,0,0),(randAppleX,randAppleY,appleThickness,appleThickness))
                sound.play(loops=0)
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
                #pygame.display.update()

        clock.tick(fps)

    pygame.quit()
    quit()



gameLoop()