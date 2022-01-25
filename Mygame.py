import pygame

# инициализируем игру
pygame.init()
# создаем окно игры
win = pygame.display.set_mode((500, 500))
# указываем у окна его заголовок
pygame.display.set_caption("My game")
# характеристики игрока
x = 50
y = 350
widht = 96

height = 128
speed = 5

isJump = False
jumpCount = 10
# загрузка фотографий(должны быть в папке с программой) персонажа и заднего фона
walkRight = [pygame.image.load('character_malePerson_walk0.png'), pygame.image.load('character_malePerson_walk1.png'),
             pygame.image.load('character_malePerson_walk2.png'), pygame.image.load('character_malePerson_walk3.png'),
             pygame.image.load('character_malePerson_walk4.png'), pygame.image.load('character_malePerson_walk5.png'),
             pygame.image.load('character_malePerson_walk6.png'), pygame.image.load('character_malePerson_walk7.png')]

playerStand = pygame.image.load('character_malePerson_idle.png')

playerJump = [pygame.image.load('character_malePerson_jump.png'), pygame.image.load('character_malePerson_jump.png'),
              pygame.image.load('character_malePerson_jump.png'), pygame.image.load('character_malePerson_jump.png'),
              pygame.image.load('character_malePerson_jump.png'), pygame.image.load('character_malePerson_jump.png'),
              pygame.image.load('character_malePerson_jump.png'), pygame.image.load('character_malePerson_jump.png')]

playerFall = [pygame.image.load('character_malePerson_fall.png'), pygame.image.load('character_malePerson_fall.png'),
              pygame.image.load('character_malePerson_fall.png'), pygame.image.load('character_malePerson_fall.png'),
              pygame.image.load('character_malePerson_fall.png'), pygame.image.load('character_malePerson_fall.png'),
              pygame.image.load('character_malePerson_fall.png'), pygame.image.load('character_malePerson_fall.png')]

walkLeft = [pygame.image.load('character_malePerson_walk0.png'), pygame.image.load('character_malePerson_walk1.png'),
            pygame.image.load('character_malePerson_walk2.png'), pygame.image.load('character_malePerson_walk3.png'),
            pygame.image.load('character_malePerson_walk4.png'), pygame.image.load('character_malePerson_walk5.png'),
            pygame.image.load('character_malePerson_walk6.png'), pygame.image.load('character_malePerson_walk7.png')]

bg = pygame.image.load('bg.jpg')
left = False
right = False
jump = False
fall = False
animCount = 0
lastMove = "right"
# время повторения цикла
clock = pygame.time.Clock()


# класс снаряд
class snaryad():
    def __init__(self, x, y, radius, color, facing):  # констурктор с параметрами
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.val = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)  # метод рисующий снаряд


# анимация
def drawWindow():
    # без это функции мы будем рисовать квадратом и то что он сместился не будет удаляться
    win.blit(bg, (0, 0))  # установка фона
    global animCount  # делаем переменную глобальну, она отвечает за анимацию
    if animCount + 1 >= 40:
        animCount = 0
    if left:  # анимация при движении влево
        win.blit(walkLeft[animCount // 5], (x, y))
        animCount += 1
    elif right:  # анимация при движении вправо
        win.blit(walkRight[animCount // 5], (x, y))
        animCount += 1
    elif jump:  # анимация при прижке
        win.blit(playerJump[animCount // 5], (x, y))
        animCount += 1
    elif fall:
        win.blit(playerFall[animCount // 5], (x, y))  # анимация при падении
        animCount += 1
    else:
        win.blit(playerStand, (x, y))  # анимация стояния

    for bullet in bullets:  # рисуем пули
        bullet.draw(win)
    # рисуем квадрат указываем то где мы хотим его нарисовать его цвет через RGB и координаты ширину и высоту
    # pygame.draw.rect(win, (0, 0, 255), (x, y, widht, height))
    pygame.display.update()  # после прохождения цикла меняет изображение на картинке


# движок игры
run = True
bullets = []
# выход из программы
while run:
    # каждые 100мс цикл повторяется
    clock.tick(40)
    # проверка на выход из программы если вышли то меняем на False и программа перестает работать
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # полет пуль и удаление когда вылетело 5
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.val
        else:
            bullets.pop(bullets.index(bullet))
    # описание того что долна делать программа при нажатии  на соответствующую кнопку
    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5 and facing == 1:
            bullets.append(snaryad(round(x + widht // 1.5), round(y + height // 1.3), 5, (255, 0, 0), facing))
        elif len(bullets) < 5 and facing == -1:
            bullets.append(snaryad(round(x + widht // 1.5 - 30), round(y + height // 1.3), 5, (255, 0, 0), facing))
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < 500 - widht - 5:
        x += speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        jump = False
        fall = False
        animCount = 0
    if not (isJump):
        # if keys[pygame.K_UP] and y > 5:
        # y -= speed
        # if keys[pygame.K_DOWN] and y < 500 - height - 15:
        # y += speed
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= - 10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
                jump = False
                fall = True
            elif jumpCount >= 0:
                y -= (jumpCount ** 2) / 2
                jump = True
                fall = False

            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    drawWindow()  # вызов функции рисования объектов

pygame.quit()  # выход из программы при нажатии на кноку выхода или другую
