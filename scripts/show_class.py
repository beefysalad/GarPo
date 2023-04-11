import pygame
import sys
import time
import requests
import os
# initialize Pygame
pygame.init()

url = 'http://localhost:8080/upload'
filename = "test.jpg"
filepath = os.path.join(os.getcwd(), filename)

# set window size and title
size = (400, 300)
pygame.display.set_caption("Object Detection")
screen = pygame.display.set_mode(size)
# set font
font = pygame.font.SysFont('Arial', 20)

# set colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# create yes and no buttons
yes_button = pygame.Rect(50, 150, 100, 50)
no_button = pygame.Rect(250, 150, 100, 50)

# create paper and plastic buttons
paper_button = pygame.Rect(50, 200, 100, 50)
plastic_button = pygame.Rect(250, 200, 100, 50)

# set text for buttons
yes_text = font.render("Yes", True, black)
no_text = font.render("No", True, black)
paper_text = font.render("Paper", True, black)
plastic_text = font.render("Plastic", True, black)

# flag to keep track of which buttons to display
display_paper_plastic_buttons = False

# set initial label
label_text = font.render("Label detected: ", True, black)

# set timer for automatic quit
last_interaction_time = time.time()

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # reset the timer for automatic quit
            last_interaction_time = time.time()
            # check if yes button is clicked
            if yes_button.collidepoint(event.pos):
                print("Yes button clicked")
                running = False
            # check if no button is clicked
            elif no_button.collidepoint(event.pos):
                print("No button clicked")
                display_paper_plastic_buttons = True
            # check if paper button is clicked
            elif display_paper_plastic_buttons and paper_button.collidepoint(event.pos):
                print("Paper button clicked")
                folder_name = 'paper'
                url = 'http://localhost:8080/upload?folder=' + folder_name
                files = {'image': open(filepath, 'rb')}
                response = requests.post(url, files=files)
                print(response.text)
                running = False
            # check if plastic button is clicked
            elif display_paper_plastic_buttons and plastic_button.collidepoint(event.pos):
                print("Plastic button clicked")
                folder_name = 'plastic'
                url = 'http://localhost:8080/upload?folder=' + folder_name
                files = {'image': open(filepath, 'rb')}
                response = requests.post(url, files=files)
                print(response.text)
                running = False

    # fill the screen with white color
    screen.fill(white)

    # display the label on the screen
    new_label_text = "The class detected is " + sys.argv[1] + ".Is it correct?"
    label_text = font.render(new_label_text, True, black)
    screen.blit(label_text, (50, 50))

    # display the yes and no buttons
    pygame.draw.rect(screen, green, yes_button)
    pygame.draw.rect(screen, red, no_button)
    screen.blit(yes_text, (70, 165))
    screen.blit(no_text, (280, 165))

    # display the paper and plastic buttons if flag is set to True
    if display_paper_plastic_buttons:
        pygame.draw.rect(screen, green, paper_button)
        pygame.draw.rect(screen, red, plastic_button)
        screen.blit(paper_text, (70, 215))
        screen.blit(plastic_text, (260, 215))

    # update the display
    pygame.display.flip()

    # check if the timer for automatic quit has expired
    if time.time() - last_interaction_time > 60:
        running = False

# quit Pygame
pygame.quit()
