import pygame
import random
import os
import sys



# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
file = os.path.dirname(__file__)
def play():
    # Khởi tạo pygame
    pygame.init()
    # Tạo màn hình
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chrome Dino Game")

    # Tải hình ảnh khủng long và cây xương rồng
    dino_img = pygame.image.load(os.path.join(file,'dinosaur.png'))
    cactus_img = pygame.image.load(os.path.join(file, 'tree.png'))

    # Kích thước khủng long và cây xương rồng
    DINO_SIZE = (50, 50)
    CACTUS_SIZE = (30, 50)

    # Thay đổi kích thước hình ảnh
    dino_img = pygame.transform.scale(dino_img, DINO_SIZE)
    cactus_img = pygame.transform.scale(cactus_img, CACTUS_SIZE)

    # Vị trí ban đầu của khủng long
    dino_x = 50
    dino_y = SCREEN_HEIGHT - DINO_SIZE[1] - 10

    # Tốc độ di chuyển của cây xương rồng
    cactus_speed = 5

    # Tốc độ nhảy và trọng lực
    jump_velocity = 0
    gravity = 1

    # Điểm số
    score = 0
    font = pygame.font.Font(None, 36)

    # Clock để điều khiển tốc độ khung hình
    clock = pygame.time.Clock()

    # Danh sách cây xương rồng
    cacti = []

    # Hàm tạo cây xương rồng mới
    def create_cactus():
        cactus_x = SCREEN_WIDTH
        cactus_y = SCREEN_HEIGHT - CACTUS_SIZE[1] - 10
        cacti.append({"x": cactus_x, "y": cactus_y})

    # Hàm kiểm tra va chạm
    def check_collision():
        dino_rect = pygame.Rect(dino_x, dino_y, DINO_SIZE[0], DINO_SIZE[1])
        for cactus in cacti:
            cactus_rect = pygame.Rect(cactus["x"], cactus["y"], CACTUS_SIZE[0], CACTUS_SIZE[1])
            if dino_rect.colliderect(cactus_rect):
                return True
        return False

    # Vòng lặp chính của trò chơi
    running = True
    frame_count = 0
    game_over = False

    while running:
        screen.fill(WHITE)  # Vẽ màu nền trắng thay vì background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        if not game_over:
            # Xử lý sự kiện bàn phím
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and dino_y == SCREEN_HEIGHT - DINO_SIZE[1] - 10:
                jump_velocity = -15  # Tốc độ nhảy lên

            # Áp dụng trọng lực
            jump_velocity += gravity
            dino_y += jump_velocity

            # Đảm bảo khủng long không rơi xuống dưới mặt đất
            if dino_y > SCREEN_HEIGHT - DINO_SIZE[1] - 10:
                dino_y = SCREEN_HEIGHT - DINO_SIZE[1] - 10
                jump_velocity = 0

            # Tạo cây xương rồng mới sau mỗi 100 frame
            if frame_count % 100 == 0:
                create_cactus()

            # Di chuyển cây xương rồng
            for cactus in cacti:
                cactus["x"] -= cactus_speed

            # Xóa cây xương rồng đã đi qua màn hình
            cacti = [cactus for cactus in cacti if cactus["x"] > -CACTUS_SIZE[0]]

            # Kiểm tra va chạm
            if check_collision():
                game_over = True

            # Tăng điểm số
            score += 1

            # Tăng tốc độ cây xương rồng sau mỗi 100 điểm
            if score % 100 == 0:
                cactus_speed += 1

            # Vẽ khủng long và cây xương rồng
            screen.blit(dino_img, (dino_x, dino_y))  # Vẽ khủng long
            for cactus in cacti:
                screen.blit(cactus_img, (cactus["x"], cactus["y"]))  # Vẽ cây xương rồng

        else:
            # Hiển thị màn hình kết thúc với điểm số
            game_over_text = font.render(f"Game Over! Your Score: {score}", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

            # Hiển thị thông báo nhấn phím để chơi lại
            restart_text = font.render("Press R to Restart", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))

            # Xử lý sự kiện để chơi lại
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Reset game
                game_over = False
                score = 0
                dino_y = SCREEN_HEIGHT - DINO_SIZE[1] - 10
                jump_velocity = 0
                cacti = []
                cactus_speed = 5  # Reset tốc độ cây xương rồng

        # Hiển thị điểm số
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Cập nhật màn hình
        pygame.display.update()

        # Điều khiển tốc độ khung hình
        clock.tick(30)
        frame_count += 1

    pygame.quit()

if __name__ == '__main__':
    play()