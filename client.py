import pygame
import urllib.request
import requests
import time
import queue
from threading import Thread

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ip = "192.168.0.107"
cam_port = "8080"
server_port = "8081"

joy_inputs = queue.Queue()

pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

canOpen = True


def grabber():
    global canOpen
    while(True):
        canOpen = False
        try:
            urllib.request.urlretrieve("http://{0}:{1}/?action=snapshot".format(ip, cam_port), "snapshot.jpg")
            canOpen = True
        except Exception as e:
            print("Error downloading frame")
            canOpen = False

        time.sleep(0.05)


t = Thread(target=grabber)
t.daemon = True
t.start()

needUpdate = False


def sendData(data):
    try:
        print("http://{0}:{1}/updateinputs".format(ip, server_port))
        response = requests.post("http://{0}:{1}/updateinputs".format(ip, server_port), data, timeout=0.5)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        print("Communication error")
        return None


def updateGamepad():
    global needUpdate
    while(True):
        joy_input = joy_inputs.get()
        if joy_input[0].type == pygame.JOYBUTTONDOWN:
            response = sendData({'type': joy_input[0].type})
            print("JoyButtonDown {0}".format(joy_input[0].button))
        elif joy_input[0].type == pygame.JOYBUTTONUP:
            response = sendData({'type': joy_input[0].type})
            print("JoyButtonUp {0}".format(joy_input[0].button))
        elif joy_input[0].type == pygame.JOYHATMOTION:
            response = sendData({'type': joy_input[0].type})
            print("JoyHatMotion {0} {1}".format(joy_input[0].hat, joy_input[0].value))
        else:
            print("Discarded input")

        # time.sleep(0.05)

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

        # if event.type == pygame.JOYAXISMOTION:
        #     joy_inputs.put([event.type])
        if event.type == pygame.JOYBUTTONDOWN:
            joy_inputs.put([event])
        if event.type == pygame.JOYBUTTONUP:
            joy_inputs.put([event])
        if event.type == pygame.JOYHATMOTION:
            joy_inputs.put([event])



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

