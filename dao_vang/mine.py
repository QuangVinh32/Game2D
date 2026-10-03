import pygame
import random
import math
import os


# Screen dimensions
rong = 800
dai = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
vang = (255, 255, 0)


file = os.path.dirname(__file__)

def play():
    # Initialize Pygame
    pygame.init()
    # Set up the screen
    screen = pygame.display.set_mode((rong, dai))
    pygame.display.set_caption("Dao vang")

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Fonts
    font = pygame.font.Font(None, 36)

    # Load assets
    background = pygame.image.load(os.path.join(file, "images/backgroundgold.jpg"))
    background = pygame.transform.scale(background, (rong, dai))

    gold_image = pygame.image.load(os.path.join(file, "images/kimcuong.jpg"))  # Load the gold image

    # Gold class
    class Gold(pygame.sprite.Sprite):
        def __init__(self, x, y, value, size):
            super().__init__()
            self.image = pygame.transform.scale(gold_image, (size, size))  # Scale the gold image
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.value = value
            self.size = size

    # Hook class
    class Hook:
        def __init__(self):
            self.x = rong // 2
            self.y = 30
            self.angle = 90  # Angle in degrees
            self.length = 50
            self.hook_speed = 2
            self.moving_out = False
            self.grabbed_gold = None

        def draw(self):
            end_x = self.x + math.cos(math.radians(self.angle)) * self.length
            end_y = self.y + math.sin(math.radians(self.angle)) * self.length
            pygame.draw.line(screen, vang, (self.x, self.y), (end_x, end_y), 3)
            pygame.draw.circle(screen, vang, (int(end_x), int(end_y)), 5)

        def update(self):
            if not self.moving_out:
                self.angle += self.hook_speed
                if self.angle > 135 or self.angle < 45:
                    self.hook_speed = -self.hook_speed

            else:
                # Move the hook outwards or inwards
                end_x = self.x + math.cos(math.radians(self.angle)) * self.length
                end_y = self.y + math.sin(math.radians(self.angle)) * self.length
                self.length += 5 if not self.grabbed_gold else -5

                # Kiểm tra nếu móc kéo chạm biên
                if end_x < 0 or end_x > rong or end_y < 0 or end_y > dai:
                    self.length = 50  # Đặt lại chiều dài
                    self.moving_out = False
                    self.grabbed_gold = None  # Không lấy được gì

                if self.length < 50:
                    self.length = 50
                    self.moving_out = False
                    self.grabbed_gold = None

                return end_x, end_y

    # Game variables
    gold_sprites = pygame.sprite.Group()
    for _ in range(15):
        x = random.randint(50, rong - 50)
        y = random.randint(100, dai - 50)
        value = random.randint(50, 150)
        size = random.randint(20, 40)
        gold_sprites.add(Gold(x, y, value, size))

    hook = Hook()
    score = 0
    running = True

    # Game loop
    while running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not hook.moving_out:
                hook.moving_out = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Draw and update hook
        hook.draw()
        end_position = hook.update()

        # Check for collision with gold
        if hook.moving_out and end_position:
            end_x, end_y = end_position
            for gold in gold_sprites:
                if gold.rect.collidepoint(end_x, end_y):
                    hook.grabbed_gold = gold  # Gắn vàng vào móc
                    area = gold.size * gold.size  # Diện tích của khối vàng
                    score += area // 100  # Cộng điểm theo diện tích
                    # Cộng điểm ngay khi chạm vào vàng
                    gold_sprites.remove(gold)  # Loại bỏ vàng khỏi màn hình
                    break

        # Draw gold
        gold_sprites.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    play()