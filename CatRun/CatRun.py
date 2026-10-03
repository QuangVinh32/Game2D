import pygame
import sys
import random
import os


file = os.path.dirname(__file__)

def play():

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    screen = pygame.display.set_mode((512, 768))
    pygame.display.set_caption("Mèo lụm lúa")

    activate = True
    playing = False
    speed = 2
    ranking = []

    black = (0,0,0)
    background = pygame.image.load(os.path.join(file, 'Assets/images/background.png'))
    cat1 = pygame.image.load(os.path.join(file, 'Assets/images/cat1.png'))
    cat2 = pygame.image.load(os.path.join(file, 'Assets/images/cat2.png'))
    cat_list = [cat1,cat2]
    play1 = pygame.image.load(os.path.join(file, 'Assets/images/play1.png'))
    play2 = pygame.image.load(os.path.join(file, 'Assets/images/play2.png'))
    out1 = pygame.image.load(os.path.join(file, 'Assets/images/sleep1.png'))
    out2 = pygame.image.load(os.path.join(file, 'Assets/images/sleep2.png'))
    mouse = pygame.image.load(os.path.join(file, 'Assets/images/mouse.png'))
    stone = pygame.image.load(os.path.join(file, 'Assets/images/stone.png'))
    wood = pygame.image.load(os.path.join(file, 'Assets/images/wood.png'))

    font = pygame.font.Font(os.path.join(file, 'Assets/fonts/pixelFont.ttf'), 36)

    bg_music = pygame.mixer.Sound(os.path.join(file, 'Assets/sounds/Littleroot Town.mp3'))
    bg_music.set_volume(0.25)
    bg_music.play()
    click_sound = pygame.mixer.Sound(os.path.join(file, 'Assets/sounds/click-a.ogg'))
    hit = pygame.mixer.Sound(os.path.join(file, 'Assets/sounds/sfx_hit.wav'))
    hit.set_volume(0.5)

    pygame.mouse.set_visible(False)

    x_object = [134,204,274,344]

    cat_run = pygame.USEREVENT + 1
    pygame.time.set_timer(cat_run, 150)
    obstacle_spawn = pygame.USEREVENT + 2
    pygame.time.set_timer(obstacle_spawn, 1000)
    class Buttons:
        def __init__(self, x, y, action, icon, icon_press):
            self.icon = icon
            self.icon_press = icon_press
            self.rect = self.icon.get_rect(topleft=(x,y))
            self.action = action
            self.is_pressed = False


        def draw(self):
            if self.is_pressed:
                screen.blit(self.icon_press, self.rect)
            else:
                screen.blit(self.icon, self.rect)

        def click(self):

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.is_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_pressed:
                    if self.rect.collidepoint(event.pos):
                        self.action()
                        self.is_pressed = False
                        return True
                    else:
                        self.is_pressed = False
            return False


    class Racetrack:

        def __init__(self):
            self.rect = background.get_rect(topleft=(0, 0))

        def draw(self):
            screen.blit(background, self.rect)
            screen.blit(background, self.rect.move(0, -768))

        def update(self):
            if self.rect.y >= 768:
                self.rect.y = 0
            self.rect.y += speed


    class Cat:
        def __init__(self,image):
            self.image = image
            self.action = 0
            self.road = 1
            self.rect  = self.image[self.action].get_rect(topleft=(204, 650))
            self.speed = 5
            self.score = 0

        def move(self):
            if self.rect.x < x_object[self.road]:
                self.rect.x += self.speed

            if self.rect.x > x_object[self.road]:
                self.rect.x -= self.speed
        def draw(self):
            screen.blit(self.image[self.action], self.rect)

        def print_score(self):
            score = font.render(f'{int(self.score)}', True, black)
            screen.blit(score,score.get_rect(center=(256,100)))


    class Obstacle:
        def __init__(self,image,x):
            self.image  = image
            self.rect = self.image.get_rect(topleft=(x, -50))

        def update(self):
            self.rect.y += speed

        def draw(self):
            screen.blit(self.image,self.rect)

    def start():
        nonlocal  playing,cat
        playing = True
        cat = Cat(cat_list)
        obstacles.clear()

    def out():
        nonlocal activate
        activate = False

    def draw_ranking():
        pass
    racetrack = Racetrack()
    cat = Cat(cat_list)
    play_button = Buttons(166, 350, start, play1, play2)
    out_button = Buttons(20, 20, out, out1, out2)
    buttons = [play_button,out_button]
    obstacles = []

    while activate:

        racetrack.draw()
        racetrack.update()

        if playing:
            obstacles = [ob for ob in obstacles if ob.rect.y < 768]
            for ob in obstacles:
                ob.update()
                ob.draw()
                if ob.rect.colliderect(cat.rect.move(0,10)):
                    hit.play()
                    ranking.append(cat.score)
                    ranking.sort()
                    ranking = ranking[:5]
                    playing = False

            cat.draw()
            cat.move()
            cat.score += speed/10
            cat.print_score()

        else:
            for b in buttons:
                b.draw()

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(mouse, mouse_pos)
        pygame.time.Clock().tick(120)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

            if playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and cat.road > 0:
                        cat.road -= 1
                    if event.key == pygame.K_RIGHT and cat.road < 3:
                        cat.road += 1
                if event.type == cat_run:
                    if cat.action == 0:
                        cat.action = 1
                    else:
                        cat.action = 0
                if event.type == obstacle_spawn:
                    obstacle_road = random.randint(0,3)
                    if obstacle_road == 3:
                        obstacles.append(Obstacle(stone, x_object[obstacle_road]))
                    else:
                        obstacles.append(Obstacle(random.choice([stone, wood]), x_object[obstacle_road]))
            else:
                for b in buttons:
                    b.click()

if __name__ == '__main__':
    play()