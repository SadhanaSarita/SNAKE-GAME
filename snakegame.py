import random
import pygame

pygame.mixer.init()
pygame.init()  # Initializing pygame

# Defining colors(RGB VALUES ke hisaab se hota hai)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Screen dimensions
screenw = 1000  # Width of the game window
screenl = 600   # Height of the game window

# Creating the game window
gameWindow = pygame.display.set_mode((screenw, screenl))

bgimg=pygame.image.load('bg.jpeg')
bgimg=pygame.transform.scale(bgimg,(screenw,screenl)).convert_alpha()#blit karne par bhi gme ki speed par farak nahi padega

pygame.display.set_caption("MY FIRST GAME - Mini Project")  # Game window title
pygame.display.update()

# Clock and font setup
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)  # Font for displaying text

# Function to display text on the screen
def score_screen(text, color, x, y):
    """Displays text on the screen at specified coordinates."""
    score_text = font.render(text, True, color)
    gameWindow.blit(score_text, [x, y])

# Welcome screen function
def welcome():
    """Displays the welcome screen until the player presses SPACE to start."""
    exit_game = False
    while not exit_game:
        # Clear the screen
        gameWindow.fill(white)

        # Display the welcome messages
        score_screen("WELCOME TO SNAKES", blue, 300, 200)
        score_screen("Press SPACE to PLAY", black, 300, 300)

        # Update the display
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit the game if close button is pressed
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Start the game if SPACE is pressed
  #music on ----------------------------------------------------------------------------                  
                    pygame.mixer.music.load('bgm.mp3')
                    pygame.mixer.music.play()
                    gameloop()  # Call the main game loop
                
        pygame.display.update()
        clock.tick(30)  # Control FPS for smooth rendering

# Main game loop
def gameloop():
    """The main game loop for handling gameplay."""
    # Variables
    exit_game = False  # To control the game loop
    game_over = False  # To track if the game is over
    snake_x = 70  # Initial x-coordinate of the snake
    snake_y = 90  # Initial y-coordinate of the snake
    snake_size = 20  # Size of each block of the snake
    velocity_x = 0  # Horizontal velocity of the snake
    velocity_y = 0  # Vertical velocity of the snake
    margin_x = screenw // 5  # 20% margin on left and right for food placement
    margin_y = screenl // 5  # 20% margin on top and bottom for food placement
    score = 0  # Initial score
    snakelist = []  # List to store snake body parts
    snakelength = 1  # Initial length of the snake
    HIGHSCORE = 0  # To track the highest score
#in python or any game etc we take the starting point of our canvas with coordinates(0,0)to avoid any confusion for us-the coders.. 
    # Generate starting food position
    food_x = random.randint(margin_x, screenw - margin_x - snake_size)
    food_y = random.randint(margin_y, screenl - margin_y - snake_size)
    fps = 30  # Frames per second

    # Function to plot the snake on the screen
    def plot_snake(gameWindow, color, snakelist, snake_size):
        """Plots the snake by drawing rectangles for each body part."""
        for x, y in snakelist:
            pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

    # Main game loop
    while not exit_game:
        if game_over:
            # Update the high score if the current score exceeds it
            if score * 10 > HIGHSCORE:
                HIGHSCORE = score * 10

            # Display game over screen
            gameWindow.fill(white)  # Clear the screen with white color
            score_screen("GAME OVER!! Press Enter to continue.", red, 200, 250)
            score_screen(f"Your Score: {score * 10}", green, 200, 300)
            score_screen(f"High Score: {HIGHSCORE}", blue, 200, 350)
            pygame.display.update()

            # Delay before allowing the player to restart
            pygame.time.delay(20000)  # Delay of 2 seconds (2000 ms)

            # Handle game over events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit game if close button is pressed
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Restart the game on Enter key press
                        welcome()  # Return to the welcome screen
                        return
            clock.tick(10)  # Slow loop for game over screen

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit game if close button is pressed
                    exit_game = True

                # Control snake's movement based on keypresses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:  # Move right
                        velocity_x = 6
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:  # Move left
                        velocity_x = -6
                        velocity_y = 0
                    if event.key == pygame.K_DOWN:  # Move down
                        velocity_y = 6
                        velocity_x = 0
                    if event.key == pygame.K_UP:  # Move up
                        velocity_y = -6
                        velocity_x = 0

                    # Cheat code to increase score////////////////////////
                    if event.key == pygame.K_q:
                        score += 10

        # Update snake's position
        snake_x += velocity_x
        snake_y += velocity_y

        # Check for collision with food
        if abs(snake_x - food_x) < 25 and abs(snake_y - food_y) < 25:
            score += 1  # Increase score
            # Generate new food position
            food_x = random.randint(margin_x, screenw - margin_x - snake_size)
            food_y = random.randint(margin_y, screenl - margin_y - snake_size)
            snakelength += 5  # Increase snake length

        # Clear the screen and draw all elements
        gameWindow.fill(white)# white canvas
        gameWindow.blit(bgimg,(0,0))

        pygame.draw.circle(gameWindow, red, [food_x, food_y], snake_size)  # Draw food
        score_screen("SCORE: " + str(score * 10), black, 5, 5)  # Display score
        score_screen("HIGH SCORE: " + str(HIGHSCORE), black, 700, 5)  # Display high score

        # Handle snake's body
        head = [snake_x, snake_y]  # Snake's head coordinates
        snakelist.append(head)  # Add head to the snake body list

        # Maintain snake length
        if len(snakelist) > snakelength:
            del snakelist[0]

        # Check if the snake collides with itself or the screen boundaries
        if head in snakelist[:-1] or snake_x >= screenw or snake_x < 0 or snake_y >= screenl or snake_y < 0:
            game_over = True  # Game over condition
            pygame.mixer.music.load('end1.mp3')
            pygame.mixer.music.play()

        plot_snake(gameWindow, black, snakelist, snake_size)  # Draw the snake
        pygame.display.update()  # Update the display

        clock.tick(fps)  # Control the speed of the game

# Start the game by showing the welcome screen
welcome()
pygame.quit()  # Quit pygame when the game ends
quit()  # Exit the game
