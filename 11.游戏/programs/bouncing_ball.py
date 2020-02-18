import pygame
import random
import math

# 定义窗口属性
W_NAME = "Bouncing Ball Game"
W_WIDTH = 1024
W_HEIGHT = 720
W_FPS = 30

# 定义颜色
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# 定义球的半径与初始速度
BALL_RADIUS = 20
START_SPEED = 10

# 定义板的形状
BOARD_WIDTH = 150
BOARD_HEIGHT = 10

# 板
class Board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('blood_red_bar.png')
        self.image = pygame.transform.scale(image,(BOARD_WIDTH,BOARD_HEIGHT)).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (BOARD_X, BOARD_Y)

# 球
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('ball.png')
        self.image = pygame.transform.scale(image,(BALL_RADIUS*2,BALL_RADIUS*2)).convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (CENTER_X, CENTER_Y)

# 画文字
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# 开始画面
def show_go_screen():
    screen.fill(BLACK)
    draw_text(screen, "BALL BOUNCING GAME", 64, W_WIDTH / 2, W_HEIGHT / 4)
    try:
        draw_text(screen, "Your Score: %d"%(score), 22, W_WIDTH / 2, W_HEIGHT / 2)
    except NameError:
        pass
    draw_text(screen, "Press a key to begin", 18, W_WIDTH / 2, W_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(W_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# 初始化
pygame.init()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption(W_NAME)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
board = Board()
ball = Ball()
all_sprites.add(board)
all_sprites.add(ball)

bounce_sound = pygame.mixer.Sound("ball.wav")
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

# 游戏主循环
running = True
game_over = True

while running:
    if game_over:
        show_go_screen()
        game_over = False
        score = 0

        # 初始位置与速度
        CENTER_X = int(W_WIDTH/2)
        CENTER_Y = int(2*W_HEIGHT/3)
        start_angle = math.pi/6*(1+random.random())
        SPEED_X = START_SPEED*math.cos(start_angle) 
        SPEED_Y = 0 - START_SPEED*math.sin(start_angle)
        BOARD_X = W_WIDTH/2
        BOARD_Y = W_HEIGHT-80

    # 保持刷新速度
    clock.tick(W_FPS)

    # 处理输入（事件）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            BOARD_X = event.dict['pos'][0]

    # 更新游戏变量——墙壁反弹
    CENTER_X += int(SPEED_X)
    CENTER_Y += int(SPEED_Y)
    if(CENTER_X>W_WIDTH-BALL_RADIUS):
        CENTER_X = 2*(W_WIDTH-BALL_RADIUS)-CENTER_X
        SPEED_X = -SPEED_X
    elif(CENTER_X<BALL_RADIUS):
        CENTER_X = 2*BALL_RADIUS - CENTER_X
        SPEED_X = -SPEED_X
    if(CENTER_Y>W_HEIGHT-BALL_RADIUS):
        CENTER_Y = 2*(W_HEIGHT-BALL_RADIUS)-CENTER_Y
        SPEED_Y = -SPEED_Y
    elif(CENTER_Y<BALL_RADIUS):
        CENTER_Y = 2*BALL_RADIUS - CENTER_Y
        SPEED_Y = -SPEED_Y

    # 更新游戏变量——板接球反弹
    if CENTER_Y+BALL_RADIUS>BOARD_Y:
        if(BOARD_X-BOARD_WIDTH/2<CENTER_X and BOARD_X+BOARD_WIDTH/2>CENTER_X):
            CENTER_Y = 2*BOARD_Y - CENTER_Y - 2*BALL_RADIUS
            SPEED_Y = -SPEED_Y*1.05
            SPEED_X = SPEED_X*1.05
            score += 1
            bounce_sound.play()
        else:
            game_over = True

    all_sprites.update()

    # 画界面
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # 刷新界面
    pygame.display.flip()

# 退出
pygame.quit()
