import pygame
import sys
import random
import os



# Thông số chương trình
X = 1200
Y = 800
FPS = 120
file = os.path.dirname(__file__)


def play():
    pygame.init()
    pygame.font.init()
    # Đồ họa
    icon = pygame.image.load(os.path.join(file, 'image/icon.png'))
    # Màu
    black = (0, 0, 0)
    white = (255, 255, 255)
    orange = (255, 165, 0)
    green = (35, 101, 51)
    # Nền
    background = pygame.image.load(os.path.join(file, 'image/background.jpg'))
    background = pygame.transform.scale(background, (X, Y))
    # Sàn
    floor = pygame.image.load(os.path.join(file, 'image/floor.png'))
    floor = pygame.transform.scale(floor, (X / 2, Y / 3.4))
    # Khung, bảng
    menu = pygame.image.load(os.path.join(file, 'image/menu.png'))
    menu_ranking = pygame.transform.scale(menu, (X / 4, Y / 2))
    menu_revive = pygame.transform.scale(menu, (X / 2.5, Y / 4))
    menu_mode = pygame.transform.scale(menu, (X / 6, Y / 8))
    coin_board = pygame.image.load(os.path.join(file, 'image/coin-board.png'))
    coin_board = pygame.transform.scale(coin_board, (X / 6.7, Y / 10))
    # Nút
    v1_button = pygame.image.load(os.path.join(file, 'image/V1.png'))
    v2_button = pygame.image.load(os.path.join(file, 'image/V2.png'))
    v_button = [v1_button, v2_button]
    x1_button = pygame.image.load(os.path.join(file, 'image/X1.png'))
    x2_button = pygame.image.load(os.path.join(file, 'image/X2.png'))
    x_button = [x1_button, x2_button]
    # Chim
    pengu_up = pygame.image.load(os.path.join(file, 'image/pengu-up.png'))
    pengu_mid = pygame.image.load(os.path.join(file, 'image/pengu-mid.png'))
    pengu_down = pygame.image.load(os.path.join(file, 'image/pengu-down.png'))
    pengu_list = [pengu_up, pengu_mid, pengu_down]
    # Ống
    pipe = pygame.image.load(os.path.join(file, 'image/pipe.png'))
    pipe = pygame.transform.scale(pipe, (X / 12, Y * 0.81))
    flip_pipe = pygame.transform.flip(pipe, True, True)
    # Xu
    coin1 = pygame.image.load(os.path.join(file, 'image/coin1.png'))
    coin2 = pygame.image.load(os.path.join(file, 'image/coin2.png'))
    coin3 = pygame.image.load(os.path.join(file, 'image/coin3.png'))
    coin4 = pygame.image.load(os.path.join(file, 'image/coin4.png'))
    coin5 = pygame.image.load(os.path.join(file, 'image/coin5.png'))
    coin6 = pygame.image.load(os.path.join(file, 'image/coin6.png'))
    status_coin = 0
    coins = [coin1, coin2, coin3, coin4, coin5, coin6, ]

    # Âm thanh
    jump_sound = pygame.mixer.Sound(os.path.join(file, 'sound/sfx_swooshing.wav'))
    coin_sound = pygame.mixer.Sound(os.path.join(file, 'sound/sfx_point.wav'))
    hit_sound = pygame.mixer.Sound(os.path.join(file, 'sound/sfx_hit.wav'))
    score_sound = pygame.mixer.Sound(os.path.join(file, 'sound/sfx_wing.wav'))
    click_sound = pygame.mixer.Sound(os.path.join(file, 'sound/switch-a.ogg'))
    # Font
    font1 = pygame.font.Font(os.path.join(file, 'Fonts/04B_19.ttf'), 36)
    font2 = pygame.font.Font(os.path.join(file, 'Fonts/pixelFont-7-8x14-sproutLands.ttf'), 36)
    font3 = pygame.font.Font(os.path.join(file, 'Fonts/pixelFont-7-8x14-sproutLands.ttf'), 18)
    font4 = pygame.font.Font(os.path.join(file, 'Fonts/pixelFont-7-8x14-sproutLands.ttf'), 16)
    # Khởi tạo chương trình
    screen = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("Cánh cụt phiêu lưu")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    # Thông số vật lí
    gravity = Y / 4000
    pipe_speed = X / 300

    # Thông số game
    difficulty_factor = 1
    difficulty_now = 'Normal'
    data_in =  open(os.path.join(file,'save.txt'), 'r')
    coins_owned = int(data_in.readline().strip())
    score_list = list(map(int, data_in.readline().split()))
    revive_cost = 15
    revive = False
    game_active = False

    # Tạo sự kiện
    spawn_pipe = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_pipe, 1500)

    spawn_coin = pygame.USEREVENT + 2
    pygame.time.set_timer(spawn_coin, 4200)
    coin_flip = pygame.USEREVENT + 3
    pygame.time.set_timer(coin_flip, 200)


    # Đối tượng trong game
    # Cụt
    class Penguin:

        def __init__(self, x, y):
            self.status = 0
            self.pengu = pengu_list[self.status]
            self.pengu = pygame.transform.scale(self.pengu, (X / 17.6, Y / 11))
            self.rect = self.pengu.get_rect(center=(x, y))
            self.speed = 0
            self.jump_height = Y/134

        def jump(self):
            self.speed = 0
            self.speed -= self.jump_height

        def draw(self):
            screen.blit(self.pengu, self.rect)

        def falling(self):
            self.speed += gravity
            self.rect.centery += self.speed

        def status_change(self):
            if self.speed < 0:
                self.status = 0
            elif self.speed <= gravity * 10:
                self.status = 1
            else:
                self.status = 2
            self.pengu = pengu_list[self.status]
            self.pengu = pygame.transform.scale(self.pengu, (X / 17.6, Y / 11))


    # Ống
    class Pipe:
        def __init__(self):
            self.y = random.randint(int(Y*0.25), int(Y*0.8))
            
            self.bot_rect = pipe.get_rect(midtop=(X*1.1, self.y))
            self.top_rect = pipe.get_rect(midbottom=(X * 1.1, self.y - Y/4))
            self.passed = True

        def draw(self):
            screen.blit(pipe, self.bot_rect)
            screen.blit(flip_pipe, self.top_rect)

        def move(self):
            self.bot_rect.x -= pipe_speed
            self.top_rect.x -= pipe_speed


    # Xu
    class ObjectCoin:
        def __init__(self):
            self.x = X * 1.1
            self.y = random.randint(int(Y * 0.25), int(Y * 0.7))
            self.c_rect = coini.get_rect(center=(self.x, self.y))

        def draw(self):
            screen.blit(coini, self.c_rect)


        def move(self):
            self.c_rect.x -= X/400


    # Sàn
    class Floor:

        def __init__(self):
            self.rect = floor.get_rect(topleft=(0, Y * 0.87))
            self.speed = X/600

        def draw(self):
            screen.blit(floor, self.rect)
            screen.blit(floor, self.rect.move(X/2, 0))
            screen.blit(floor, self.rect.move(X, 0))

        def update(self):
            self.rect.x -= self.speed
            if self.rect.x <= -X / 2:
                self.rect.x = 0


    class Score:
        def __init__(self, s_list):
            self.now = 0
            self.ranking = s_list
            self.board_rect = menu_ranking.get_rect(center=(X/1.96, Y/2))


        def print_score(self):
            print_score = font1.render(f'{self.now}', True, white, black)
            rect = print_score.get_rect(center=(X * 0.5, Y * 0.15))
            screen.blit(print_score, rect)

        def update(self):
            self.ranking.append(self.now)
            self.ranking.sort(reverse=True)
            self.ranking = self.ranking[0:5]

        def draw_ranking(self):
            screen.blit(menu_ranking, self.board_rect)
            for t in range(len(self.ranking)):
                rank = font2.render(f'Top {t+1} : {self.ranking[t]}', True, black)
                rank_rect = rank.get_rect(center=self.board_rect.midtop)
                screen.blit(rank, rank_rect.move(0, (t+1)*(Y/12)))


    class UseCoins:
        def __init__(self, now):
            self.now = now


        def draw(self):
            print_coin = font1.render(f': {self.now} ', True, orange)
            screen.blit(coin_board, (X * 0.84, Y * 0.053))
            screen.blit(coini, (X * 0.85, Y * 0.07))
            screen.blit(print_coin, (X * 0.9, Y * 0.083))

    class Button:
        def __init__(self,x ,y, b_list):
            self.status = 0
            self.list = b_list
            self.button = self.list[self.status]
            self.button = pygame.transform.scale(self.button, (X / 16, Y / 10))
            self.rect = self.button.get_rect(center=(x, y))

        def draw(self):
            screen.blit(self.button, self.rect)

        def click(self):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.status = 1
                    self.button = self.list[self.status]
                    self.button = pygame.transform.scale(self.button, (X / 16, Y / 10))
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.status:
                    self.status = 0
                    self.button = self.list[self.status]
                    self.button = pygame.transform.scale(self.button, (X / 16, Y / 10))
                    return True
            return False


    def draw_revie_ask():
        ask = font2.render('Do you want to revie?', True, black)
        cost = font2.render(f'(Cost : {revive_cost} Coins)', True, green)
        ask_revie_rect = menu_revive.get_rect(center=(X / 1.96, Y / 2.5))
        ask_rect = ask.get_rect(midtop=ask_revie_rect.midtop).move(0,20)
        cost_rect = cost.get_rect(midtop=ask_rect.midtop).move(0,40)
        screen.blit(menu_revive, ask_revie_rect)
        screen.blit(ask, ask_rect)
        screen.blit(cost, cost_rect)

    def pick_mode():
        mode_ask = font3.render('Pick mode:', True, black)
        mode = font4.render('1.Easy  2.Normal  3.Hard', True, black)
        mode_now = font4.render('Mode now:', True, black)
        mode_pick = font4.render(f'{difficulty_now}', True, green)
        screen.blit(menu_mode, (0, 0))
        screen.blit(mode_ask, (X/120, Y/80))
        screen.blit(mode, (X/120, Y/20))
        screen.blit(mode_now, (X/120, Y/11))
        screen.blit(mode_pick, (X/12, Y/11))

    # Khởi tạo đối tượng
    piplup = Penguin(X / 5, Y / 2)
    floors = Floor()
    pipe_list = []
    coin_list = []
    button_list = [Button(X*0.39, Y/2.15, x_button),Button(X*0.63, Y/2.15, v_button)]
    score = Score(score_list)
    value_coin = UseCoins(coins_owned)
    # Vòng lặp chính
    run = True
    while run:
        coini = coins[status_coin]
        coini = pygame.transform.scale(coini, (X / 25, Y / 15))
        # Xóa đối tượng đã ra khỏi màn hình
        coin_list = [coin for coin in coin_list if coin.c_rect.x > -X*0.1]
        pipe_list = [pipe for pipe in pipe_list if pipe.bot_rect.x > -X*0.1]

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    data_out = open(os.path.join(file, 'save.txt'), 'w')
                    data_out.write(f'{value_coin.now}\n')
                    data_out.write(' '.join(map(str, score.ranking)))
                    run = False
                if game_active:
                    if event.key == pygame.K_SPACE:
                        jump_sound.play()
                        piplup.jump()
                elif revive and value_coin.now >= revive_cost:
                    if event.key == pygame.K_y:
                        piplup = Penguin(X / 5, Y / 2)
                        value_coin.now -= revive_cost
                        coin_list.clear()
                        pipe_list.clear()
                        game_active = True
                        revive = False
                    if event.key == pygame.K_n:
                        revive = False
                else:
                    if event.key == pygame.K_SPACE:
                        pipe_speed = (X / 300) * difficulty_factor
                        pipe_list.clear()
                        coin_list.clear()
                        piplup = Penguin(X / 5, Y / 2)
                        score = Score(score_list)
                        revive = True
                        game_active = True
                    if event.key == pygame.K_1:
                        difficulty_factor = 0.75
                        difficulty_now = 'Easy'
                    if event.key == pygame.K_2:
                        difficulty_factor = 1
                        difficulty_now = 'Normal'
                    if event.key == pygame.K_3:
                        difficulty_factor = 1.5
                        difficulty_now = 'Hard'
            if revive and value_coin.now >= revive_cost:
                for i in range(len(button_list)):
                    if button_list[i].click():
                        if i == 1:
                            piplup = Penguin(X / 5, Y / 2)
                            value_coin.now -= revive_cost
                            coin_list.clear()
                            pipe_list.clear()
                            game_active = True
                            revive = False
                        elif i == 0:
                            revive = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

            if event.type == pygame.QUIT:
                data_out = open(os.path.join(file,'save.txt'), 'w')
                data_out.write(f'{value_coin.now}\n')
                data_out.write(' '.join(map(str, score.ranking)))
                pygame.quit()
                sys.exit()

            if event.type == spawn_pipe:
                pipe_list.append(Pipe())
                if 1500 - score.now * 2 >= 500:
                    pygame.time.set_timer(spawn_pipe, 1500 - score.now * 2)

            if event.type == spawn_coin:
                coin_list.append(ObjectCoin())

            if event.type == coin_flip:
                if status_coin < 5:
                    status_coin += 1
                else:
                    status_coin = 0

        screen.blit(background, (0, 0))

        if game_active:
            # Hoạt động của cụt
            piplup.status_change()
            piplup.falling()
            piplup.draw()
            if 0 > piplup.rect.y or piplup.rect.y > Y * 0.8:
                hit_sound.play()
                game_active = False
                score.update()
            # Hoạt động của ống
            for pi in pipe_list:
                pi.move()
                # Kiểm tra va chạm với chim
                if piplup.rect.colliderect(pi.top_rect) or piplup.rect.colliderect(pi.bot_rect):
                    score.update()
                    hit_sound.play()
                    game_active = False
                # Kiểm tra tính điểm
                if pi.passed and pi.top_rect.x < piplup.rect.x:
                    score.now += 1
                    pipe_speed = (X * (1 + score.now / 110) / 300) * difficulty_factor
                    score_sound.play()
                    pi.passed = False
                pi.draw()
            # Hoạt động của xu
            score.print_score()
            for coin in coin_list:
                coin.move()
                if piplup.rect.colliderect(coin.c_rect):
                    value_coin.now += 1
                    coin_sound.play()
                    coin_list.remove(coin)
                coin.draw()
        elif revive and value_coin.now >= revive_cost:
            draw_revie_ask()
            for b in button_list:
                b.draw()
        else:
            pick_mode()
            score.draw_ranking()

        # Hiển thị xu đang có
        value_coin.draw()
        # Hoạt động của sàn
        floors.draw()
        floors.update()
        # Hoạt động của chương trình
        pygame.display.update()
        clock.tick(FPS)
if __name__ == '__main__':
    play()