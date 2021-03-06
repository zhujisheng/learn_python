import pygame
import random
import math
import sys

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
    def __init__(self, width, height, init_x, init_y):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.x = init_x
        self.y = init_y
        image = pygame.image.load('blood_red_bar.png')
        self.image = pygame.transform.scale(image,(width,height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        # 板运动
        self.x = pygame.mouse.get_pos()[0]
        self.rect.center = (self.x, self.y)

# 球
class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, init_x, init_y, init_speed_x, init_speed_y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.x = init_x
        self.y = init_y
        self.speed_x = init_speed_x
        self.speed_y = init_speed_y
        image = pygame.image.load('ball.png')
        self.image = pygame.transform.scale(image,(radius*2,radius*2)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        # 球运动
        self.x += int(self.speed_x)
        self.y += int(self.speed_y)
        if(self.x>W_WIDTH-self.radius):
            self.x = 2*(W_WIDTH-self.radius)-self.x
            self.speed_x = -self.speed_x
        elif(self.x<self.radius):
            self.x = 2*self.radius - self.x
            self.speed_x = -self.speed_x
        if(self.y>W_HEIGHT-self.radius):
            self.y = 2*(W_HEIGHT-self.radius)-self.y
            self.speed_y = -self.speed_y
        elif(self.y<self.radius):
            self.y = 2*self.radius - self.y
            self.speed_y = -self.speed_y

        self.rect.center = (self.x, self.y)


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
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# 初始化
pygame.init()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption(W_NAME)
clock = pygame.time.Clock()

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

        # 初始化球与板
        all_sprites = pygame.sprite.Group()
        board = Board(BOARD_WIDTH, BOARD_HEIGHT, W_WIDTH/2, W_HEIGHT-80)
        start_angle = math.pi/6*(1+random.random())
        ball = Ball(BALL_RADIUS, int(W_WIDTH/2), int(2*W_HEIGHT/3), START_SPEED*math.cos(start_angle), -START_SPEED*math.sin(start_angle))
        all_sprites.add(board)
        all_sprites.add(ball)

    # 保持刷新速度
    clock.tick(W_FPS)

    # 处理输入（事件）
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新游戏变量
    all_sprites.update()

    # 发生碰撞
    if pygame.sprite.collide_rect(ball, board) and ball.y>board.y-ball.radius:
        ball.y = 2*board.y - ball.y - 2*ball.radius
        ball.speed_y = -ball.speed_y*1.05
        ball.speed_x = ball.speed_x*1.05
        score += 1
        bounce_sound.play()

    # 掉落
    if ball.y > board.y:
        game_over = True

    # 画界面
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # 刷新界面
    pygame.display.flip()

# 退出
pygame.quit()
