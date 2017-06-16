import pygame
import urllib.request
import urllib.parse
import time
import queue
from threading import Thread

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

inputs = queue.Queue()

pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

canOpen = True


def grabber():
    global canOpen
    while(True):
        canOpen = False
        try:
            urllib.request.urlretrieve("http://192.168.137.4:8080/?action=snapshot", "snapshot.jpg")
            canOpen = True
        except:
            canOpen = False

        time.sleep(0.1)


t = Thread(target=grabber)
t.daemon = True
t.start()

needUpdate = False


def updateGamepad():
    global needUpdate
    while(True):
        if needUpdate:
            try:
                input = inputs.get()
                if input[0] == "button":
                    data = urllib.parse.urlencode({'joysticks': {1: True, 2: False}, 'buttons': {1: False, 2: True}}, data)
                    response = urllib.request.urlopen("http://192.168.137.4:8080/updateinputs")
                    print(response.read())
            except:
                pass
            needUpdate = False

        time.sleep(0.3)

t2 = Thread(target=updateGamepad)
t2.daemon = True
t2.start()


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 490
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


# Set the width and height of the screen [width,height]
size = [640, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("piROV")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks


for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

image = pygame.image.load("placeholder.png")
canOpen = False

textPrint = TextPrint()

while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION

        if event.type == pygame.JOYAXISMOTION:
            needUpdate = True
        if event.type == pygame.JOYBUTTONDOWN:
            needUpdate = True
        if event.type == pygame.JOYBUTTONUP:
            needUpdate = True
            input.put(["button"])
        if event.type == pygame.JOYHATMOTION:
            needUpdate = True



    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    if canOpen:
        try:
            image = pygame.image.load("snapshot.jpg")
        except:
            pass
    screen.blit(image, (0, 0))

    textPrint.print(screen, "Esto es ua prueba")
    textPrint.print(screen, "Esto es ua prueba 2")

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 30 frames per second
    clock.tick(30)

pygame.quit()

