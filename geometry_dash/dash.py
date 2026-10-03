import pygame
import random
import sys
import os

# Constants
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 50
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 50  # Smaller height to fit on the floor
GRAVITY = 0.5
JUMP_STRENGTH = -15
BACKGROUND_COLOR = (255, 255, 255)
FLOOR_HEIGHT = HEIGHT - 50  # Height where the thorns will be placed (near the floor)
file = os.path.dirname(__file__)
def play():
    # Initialize Pygame
    pygame.init()
    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Geometry Dash')

    # Load images
    background = pygame.image.load(os.path.join(file,"background.jpg"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Resize to fit the screen
    cube_image = pygame.image.load(os.path.join(file,"cube.png"))
    cube_image = pygame.transform.scale(cube_image, (SQUARE_SIZE, SQUARE_SIZE))  # Resize player image
    thorn_image = pygame.image.load(os.path.join(file,"thorn.png"))
    thorn_image = pygame.transform.scale(thorn_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))  # Resize thorn image

    # Player class (cube)
    class Player:
        def __init__(self):
            self.x = 50
            self.y = HEIGHT - SQUARE_SIZE - 50
            self.width = SQUARE_SIZE
            self.height = SQUARE_SIZE
            self.velocity = 0
            self.is_jumping = False

        def jump(self):
            if not self.is_jumping:
                self.velocity = JUMP_STRENGTH
                self.is_jumping = True

        def update(self):
            self.velocity += GRAVITY
            self.y += self.velocity
            if self.y > HEIGHT - SQUARE_SIZE - 50:
                self.y = HEIGHT - SQUARE_SIZE - 50
                self.velocity = 0
                self.is_jumping = False

        def draw(self):
            screen.blit(cube_image, (self.x, self.y))  # Draw the play  er cube

    # Obstacle class (thorn)
    class Obstacle:
        def __init__(self):
            self.x = WIDTH
            self.y = FLOOR_HEIGHT - OBSTACLE_HEIGHT  # Set the y-coordinate of the thorn on the floor
            self.width = OBSTACLE_WIDTH
            self.height = OBSTACLE_HEIGHT
            self.image = thorn_image  # Use thorn image

        def move(self):
            self.x -= 5  # Move obstacle leftwards

        def draw(self):
            screen.blit(self.image, (self.x, self.y))  # Draw the thorn obstacle at the floor

        def off_screen(self):
            return self.x < -self.width  # Check if the obstacle is off-screen

        def collide(self, player):
            # Check if the player collides with the obstacle
            return (self.x < player.x + player.width and
                    self.x + self.width > player.x and
                    self.y < player.y + player.height)

    # Game loop
    def game_loop():
        player = Player()
        obstacles = []
        clock = pygame.time.Clock()
        score = 0
        running = True

        while running:
            screen.blit(background, (0, 0))  # Draw background image

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.jump()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    nonlocal t
                    t = False
                    running = False

            # Update game elements
            player.update()

            # Create new obstacles
            if random.randint(1, 100) <= 2:  # Probability of spawning a new obstacle
                obstacles.append(Obstacle())

            # Move obstacles and remove off-screen ones
            for obstacle in obstacles[:]:
                obstacle.move()
                if obstacle.off_screen():
                    obstacles.remove(obstacle)
                    score += 1  # Increase score when an obstacle moves off the screen

            # Check for collisions
            for obstacle in obstacles:
                if obstacle.collide(player):
                    running = False  # End the game if collision happens

            # Draw obstacles
            for obstacle in obstacles:
                obstacle.draw()

            # Draw the player
            player.draw()

            # Draw the score
            font = pygame.font.SysFont("Arial", 24)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.update()  # Update the screen
            clock.tick(60)  # Limit FPS to 60

    # Start the game
    t = True
    while t:
        game_loop()

    # Quit Pygame
    pygame.quit()
if __name__ == '__main__':
    play()