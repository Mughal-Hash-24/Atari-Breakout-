import pygame, random, math

pygame.init()
# pygame.key.set_colorkey((0,0,0))
clock = pygame.time.Clock()

win_res = (800, 600)

red = (255,114,118)
blue = (5,195,221)
green = (0,168,107)

colors = [red, blue, green]

window = pygame.display.set_mode(win_res)

bg_color = (240, 240, 240)

matrix = []

class Pad(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((200, 25))
        self.image.fill((60, 60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 565
        self.vel = 10

    def move_left(self):
        self.rect.x -= self.vel

    def move_right(self):
        self.rect.x += self.vel

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0,0,0), (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (win_res[0]/2, win_res[1]/2)
        self.vel = 4 
        self.angle = (math.pi)/3

    def update(self):
        self.rect.x += self.vel * math.cos(self.angle)
        self.rect.y -= self.vel * math.sin(self.angle)

        if self.rect.x <= 0 or self.rect.x >= win_res[0]-20:
            self.angle = math.pi - self.angle
        if self.rect.y <= 0:
            self.angle = -self.angle
        if self.rect.y >= win_res[1] - 20:
            pygame.quit()

def generate_level():
    rows = 6
    columns = 10

    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(random.randint(0,2))
    
        matrix.append(row)
    return matrix

class Map(pygame.sprite.Sprite):
    def __init__(self, matrix, colors, start_x, start_y):
        super().__init__()
        self.image = pygame.Surface((1200, 280))
        self.rect = self.image.get_rect()
        self.matrix = matrix
        self.colors = colors
        self.start_x = start_x
        self.start_y = start_y

    def generate_map(self):
        rects = []
        for y in self.matrix:
            self.start_x = 30  # Reset x-coordinate for each row
            for x in y:
                rect = pygame.Rect(self.start_x, self.start_y, 100, 50)
                rects.append((rect, self.colors[x]))  # Store the rect and color
                self.start_x += 115  # Increment x-coordinate for the next tile
            self.start_y += 65  # Increment y-coordinate for the next row
        return rects             

def game_loop():

    pad = Pad()

    ball = Ball()

    all_sprites = pygame.sprite.Group()

    all_sprites.add(pad)
    all_sprites.add(ball)

    generate_level()

    tiles = Map(matrix, colors, 30, 10)
    rects = tiles.generate_map()

    # all_sprites.add(tiles)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and pad.rect.x > 0:
            pad.move_left()

        elif keys[pygame.K_RIGHT] and pad.rect.x < win_res[0] - 200:
            pad.move_right()

        if (ball.rect.x >= pad.rect.x and ball.rect.x <= pad.rect.x + 200):
            if ball.rect.y+20>=pad.rect.y:
                dist = (ball.rect.centerx - pad.rect.centerx)/100
                max_angle = 45
                angle = max_angle*dist
                angle_radians = math.radians(angle)
                if dist > 0:
                    ball.angle = -ball.angle - angle_radians
                if dist < 0:
                    ball.angle = -ball.angle - angle_radians


        for rect, color in rects.copy():
            if ball.rect.colliderect(rect):
                rects.remove((rect, color))
                ball.angle = -ball.angle

        window.fill(bg_color)
        ball.update()
        all_sprites.draw(window)

        for rect, color in rects:  # Draw the pre-generated rects
            pygame.draw.rect(window, color, rect)
        all_sprites.update()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

game_loop()