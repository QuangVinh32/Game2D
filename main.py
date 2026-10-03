from flappy import flappy
from dao_vang import mine
from CatRun import CatRun
from geometry_dash import dash
from dino import dino
import vision
import multiprocessing
import pygame
import sys


program = 0

process1 = multiprocessing.Process(target=vision.play)

def main_program():
    pygame.init()
    pygame.font.init()
    global program

    screen = pygame.display.set_mode((738, 670))
    pygame.display.set_caption("Game Center")


    fps = 30

    white = (255,255,255)
    bg = pygame.image.load('asset/UI/background.png')
    ic1 = pygame.image.load('asset/UI/flapp_icon.png')
    ic2 = pygame.image.load('asset/UI/daovang_icon.png')
    ic3 = pygame.image.load('asset/UI/cat_icon.png')
    ic4 = pygame.image.load('asset/UI/dash_icon.png')
    ic5 = pygame.image.load('asset/UI/dino_icon.png')

    font1 = pygame.font.Font('asset/Fonts/FRESHFACE.ttf', 72)
    text1 = font1.render('Game Center', True, white)

    class Buttons:
        def __init__(self, x, y, action, icon,n):
            self.icon = icon
            self.rect = self.icon.get_rect(topleft=(x, y))
            self.action = action
            self.n = n
            self.is_pressed = False

        def draw(self):
            screen.blit(self.icon, self.rect)

        def click(self):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.is_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_pressed:
                    if self.rect.collidepoint(event.pos):
                        self.action(self.n)
                        self.is_pressed = False
                        return True
                    else:
                        self.is_pressed = False
            return False

    def change(n):
        global program
        pygame.quit()
        program = n

    b1 = Buttons(100,250,change,ic1,1)
    b2 = Buttons(300, 250, change, ic2,2)
    b3 = Buttons(500, 250, change, ic3,3)
    b4 = Buttons(100, 450, change, ic4,4)
    b5 = Buttons(300, 450, change, ic5,5)
    buttons = [b1,b2,b3,b4,b5]
    while program == 0:
        screen.blit(bg, (0,0))
        screen.blit(text1, (155,140))
        for b in buttons:
            b.draw()
        pygame.time.Clock().tick(fps)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    process1.start()
                if event.key == pygame.K_k:
                    process1.terminate()

            for b in buttons:
                b.click()



def return_main():
    global program
    pygame.quit()
    program = 0
    program_run()

def program_run():
    global program
    pygame.quit()
    if program == 0:
        main_program()

    if program == 1:
        flappy.play()

    if program == 2:
        mine.play()

    if program == 3:
        CatRun.play()

    if program == 4:
        dash.play()

    if program == 5:
        dino.play()

    return_main()
if __name__ == '__main__':
    program_run()

