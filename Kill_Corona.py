# IMPORT
import pygame
import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import time

# INITIALIZE
pygame.init()

# CREATE WINDOW
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kill Corona")

# FPS
FPS = 30 #This is becuase our webcam is 30fps
clock = pygame.time.Clock()

# VARIABLES
velocity = 5
score = 0
start_time = time.time()
game_time = 10

# HAND DETECTION
detector = HandDetector(detectionCon=0.7,maxHands=1)

# INITIALIZE WEBCAM
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #WIDTH
cap.set(4, 720) #HEIGHT

# LOAD IMAGES
corona_image = pygame.image.load("./Resources/red_corona_2.png").convert_alpha()
corona_image = pygame.transform.scale(corona_image, (300, 300))
rect_corona = corona_image.get_rect()
rect_corona.x, rect_corona.y = 500, 300

# FUNCTIONS
def reset_corona():
    rect_corona.x = random.randint(100, img.shape[1] - 100)
    rect_corona.y = img.shape[0] + 50

# LOOP
run = True
while run:

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # GAME LOGIC and DRAWINGS
    time_remaining = int(game_time - (time.time() - start_time))
    if time_remaining  < 0:
        WIN.fill((255,255,255))

    # OpenCV
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # MOVE CORONA ABOVE
    rect_corona.y -= velocity

    # CORONA REACHING TOP AND RSETING TO NEW POSITION
    if rect_corona.y < 0:
        reset_corona()
        velocity += 2

    if hands:
        hand = hands[0]
        x, y = hand['lmList'][4]
        a, b = hand['lmList'][8]
        c, d = hand['lmList'][12]
        e, f = hand['lmList'][16]
        g, h = hand['lmList'][20]

        #print(hand['lmList'][8] < hand['lmList'][5])
        if rect_corona.collidepoint(a, b):
            #print(rect_corona.collidepoint(x, y))
            reset_corona()
            velocity += 2
            score += 10

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    
    # DRAWINGS
    WIN.blit(frame, (0,0))
    WIN.blit(corona_image, (rect_corona))
    font = pygame.font.Font(None, 50)
    point = font.render(f"Total Corona Killed: {score}", True, (255, 0, 0))
    #time_s = font.render(f"Time: {time_remaining}", True, (255, 255, 255))
    WIN.blit(point, (10, 10))
    #WIN.blit(time_s, (10, 100))
    #pygame.draw.rect(WIN, (255,0,0), rect_corona)

    # UPDATE DISPLAY/WINDOW
    pygame.display.update()

    # FINALIZING FPS
    clock.tick(FPS)