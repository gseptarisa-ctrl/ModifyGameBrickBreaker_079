
import pygame
import random
import math
import sys

pygame.init()

# =====================================================
# CONFIGURATION
# =====================================================

WIDTH, HEIGHT = 600, 500
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello Kitty Pink Brick Breaker")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 15, bold=True)
small_font = pygame.font.SysFont("Arial", 12, bold=True)
large_font = pygame.font.SysFont("Arial", 32, bold=True)

WHITE = (255, 255, 255)
PINK = (255, 85, 165)
BABY_PINK = (255, 185, 220)
LIGHT_PINK = (255, 220, 240)
LAVENDER = (211, 160, 245)
PURPLE = (139, 70, 135)
DARK_PURPLE = (65, 28, 65)
GOLD = (255, 205, 80)


# =====================================================
# BACKGROUND
# =====================================================

def create_background():

    surface = pygame.Surface((WIDTH, HEIGHT))

    top = (105, 52, 115)
    bottom = (255, 145, 205)

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        color = tuple(
            int(top[i] * (1 - ratio) + bottom[i] * ratio)
            for i in range(3)
        )

        pygame.draw.line(
            surface,
            color,
            (0, y),
            (WIDTH, y)
        )

    return surface


background = create_background()


# =====================================================
# DECORATIONS
# =====================================================

random.seed(12)

stars = [
    (
        random.randint(15, WIDTH - 15),
        random.randint(70, HEIGHT - 20),
        random.randint(2, 4)
    )
    for _ in range(45)
]


def draw_star(surface, x, y, size, color):

    points = []

    for i in range(10):

        angle = -math.pi / 2 + i * math.pi / 5

        radius = size if i % 2 == 0 else size * 0.4

        points.append((
            x + math.cos(angle) * radius,
            y + math.sin(angle) * radius
        ))

    pygame.draw.polygon(surface, color, points)


def draw_heart(surface, x, y, size, color):

    points = [
        (x, y + size * 0.85),
        (x - size, y - size * 0.05),
        (x - size * 0.95, y - size * 0.65),
        (x - size * 0.4, y - size * 0.8),
        (x, y - size * 0.35),
        (x + size * 0.4, y - size * 0.8),
        (x + size * 0.95, y - size * 0.65),
        (x + size, y - size * 0.05)
    ]

    pygame.draw.polygon(surface, color, points)


def draw_cloud(surface, x, y, scale=1):

    color = (255, 210, 235)

    pygame.draw.circle(
        surface,
        color,
        (int(x), int(y)),
        int(27 * scale)
    )

    pygame.draw.circle(
        surface,
        color,
        (int(x + 28 * scale), int(y - 12 * scale)),
        int(34 * scale)
    )

    pygame.draw.circle(
        surface,
        color,
        (int(x + 60 * scale), int(y)),
        int(27 * scale)
    )

    pygame.draw.rect(
        surface,
        color,
        (
            int(x - 25 * scale),
            int(y - 5 * scale),
            int(110 * scale),
            int(30 * scale)
        )
    )


def draw_background():

    screen.blit(background, (0, 0))

    for x, y, size in stars:

        draw_star(
            screen,
            x,
            y,
            size,
            (255, 235, 255)
        )

    draw_heart(screen, 45, 180, 10, BABY_PINK)
    draw_heart(screen, 555, 190, 12, BABY_PINK)
    draw_heart(screen, 85, 325, 8, LIGHT_PINK)
    draw_heart(screen, 520, 340, 9, LIGHT_PINK)

    draw_cloud(screen, -20, 475, 1.3)
    draw_cloud(screen, 445, 480, 1.3)

    # Decorative bow
    pygame.draw.ellipse(
        screen,
        PINK,
        (470, 435, 45, 35)
    )

    pygame.draw.ellipse(
        screen,
        PINK,
        (510, 435, 45, 35)
    )

    pygame.draw.circle(
        screen,
        LIGHT_PINK,
        (510, 452),
        9
    )


# =====================================================
# GLOSSY DRAWING
# =====================================================

def draw_glossy_rect(surface, rect, color, radius=8):

    shadow = rect.copy()
    shadow.y += 3

    pygame.draw.rect(
        surface,
        DARK_PURPLE,
        shadow,
        border_radius=radius
    )

    pygame.draw.rect(
        surface,
        color,
        rect,
        border_radius=radius
    )

    highlight = pygame.Rect(
        rect.x + 4,
        rect.y + 3,
        rect.width - 8,
        4
    )

    pygame.draw.rect(
        surface,
        WHITE,
        highlight,
        border_radius=3
    )


# =====================================================
# INDIVIDUAL HELLO KITTY BLOCK
# =====================================================

class Block:

    def __init__(self, x, y, color):

        self.rect = pygame.Rect(x, y, 48, 40)

        self.color = color

        self.health = 1
        self.alive = True

    def hit(self):

        self.health -= 1

        if self.health <= 0:

            self.alive = False

    def display(self):

        if not self.alive:
            return

        x = self.rect.x
        y = self.rect.y

        outline = (125, 55, 110)

        # Shadow
        pygame.draw.ellipse(
            screen,
            DARK_PURPLE,
            (x + 5, y + 31, 38, 7)
        )

        # Left ear
        pygame.draw.polygon(
            screen,
            outline,
            [
                (x + 5, y + 22),
                (x + 8, y + 3),
                (x + 22, y + 14)
            ]
        )

        # Right ear
        pygame.draw.polygon(
            screen,
            outline,
            [
                (x + 27, y + 14),
                (x + 40, y + 3),
                (x + 44, y + 22)
            ]
        )

        # Inner ears
        pygame.draw.polygon(
            screen,
            BABY_PINK,
            [
                (x + 10, y + 15),
                (x + 11, y + 8),
                (x + 18, y + 14)
            ]
        )

        pygame.draw.polygon(
            screen,
            BABY_PINK,
            [
                (x + 31, y + 14),
                (x + 38, y + 8),
                (x + 39, y + 15)
            ]
        )

        # Main face outline
        pygame.draw.ellipse(
            screen,
            outline,
            (x + 3, y + 10, 43, 29)
        )

        # Main face
        pygame.draw.ellipse(
            screen,
            self.color,
            (x + 4, y + 11, 41, 27)
        )

        # Glossy highlight
        pygame.draw.ellipse(
            screen,
            WHITE,
            (x + 9, y + 13, 10, 4)
        )

        # Eyes
        pygame.draw.ellipse(
            screen,
            DARK_PURPLE,
            (x + 15, y + 23, 4, 6)
        )

        pygame.draw.ellipse(
            screen,
            DARK_PURPLE,
            (x + 31, y + 23, 4, 6)
        )

        # Nose
        pygame.draw.ellipse(
            screen,
            GOLD,
            (x + 24, y + 26, 5, 4)
        )

        # Whiskers
        for side in [-1, 1]:

            start_x = x + 8 if side == -1 else x + 42
            end_x = x + 1 if side == -1 else x + 49

            for offset in [-3, 3]:

                pygame.draw.line(
                    screen,
                    DARK_PURPLE,
                    (start_x, y + 24 + offset),
                    (end_x, y + 21 + offset),
                    1
                )

        # Pink bow
        bow_x = x + 37
        bow_y = y + 10

        pygame.draw.circle(
            screen,
            DARK_PURPLE,
            (bow_x - 5, bow_y),
            6
        )

        pygame.draw.circle(
            screen,
            DARK_PURPLE,
            (bow_x + 5, bow_y),
            6
        )

        pygame.draw.circle(
            screen,
            PINK,
            (bow_x - 5, bow_y),
            5
        )

        pygame.draw.circle(
            screen,
            PINK,
            (bow_x + 5, bow_y),
            5
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (bow_x, bow_y),
            3
        )

    def getRect(self):

        return self.rect


# =====================================================
# CREATE HELLO KITTY GRID
# =====================================================

def populateBlocks():

    blocks = []

    colors = [
        (255, 220, 240),
        (255, 105, 180),
        (215, 175, 245),
        (255, 240, 250)
    ]

    columns = 9
    rows = 5

    block_width = 48
    block_height = 40

    gap_x = 10
    gap_y = 12

    total_width = (
        columns * block_width +
        (columns - 1) * gap_x
    )

    start_x = (WIDTH - total_width) // 2

    # Space between bricks and ball
    start_y = 85

    for row in range(rows):

        for col in range(columns):

            x = start_x + col * (block_width + gap_x)

            y = start_y + row * (block_height + gap_y)

            color = colors[
                (row + col) % len(colors)
            ]

            blocks.append(
                Block(x, y, color)
            )

    return blocks


# =====================================================
# BALL CLASS WITH METEOR TRAIL
# =====================================================

class Ball:

    def __init__(self):

        self.radius = 8
        self.speed = 5

        self.trail = []

        self.reset()

    def reset(self, paddle=None):

        if paddle:

            self.x = paddle.rect.centerx

            self.y = paddle.rect.top - self.radius - 8

        else:

            self.x = WIDTH // 2
            self.y = 420

        self.dx = random.choice([-1, 1])
        self.dy = -1

        self.launched = False

        self.trail.clear()

    def launch(self):

        self.launched = True

    def getRect(self):

        return pygame.Rect(
            round(self.x - self.radius),
            round(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def update(self):

        if not self.launched:
            return False

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Save trail positions
        self.trail.append((self.x, self.y))

        if len(self.trail) > 12:

            self.trail.pop(0)

        # Left wall
        if self.x - self.radius <= 0:

            self.x = self.radius
            self.dx = abs(self.dx)

        # Right wall
        elif self.x + self.radius >= WIDTH:

            self.x = WIDTH - self.radius
            self.dx = -abs(self.dx)

        # Top wall
        if self.y - self.radius <= 0:

            self.y = self.radius
            self.dy = abs(self.dy)

        # Bottom
        if self.y - self.radius > HEIGHT:

            return True

        return False

    def display(self):

        # Meteor trail
        for i, (tx, ty) in enumerate(self.trail):

            progress = (i + 1) / len(self.trail)

            radius = max(
                2,
                int(self.radius * progress * 0.8)
            )

            color = (
                255,
                int(110 + 100 * progress),
                int(180 + 60 * progress)
            )

            pygame.draw.circle(
                screen,
                color,
                (int(tx), int(ty)),
                radius
            )

        # Outer glow
        pygame.draw.circle(
            screen,
            (255, 175, 220),
            (int(self.x), int(self.y)),
            13
        )

        # Ball
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            BABY_PINK,
            (int(self.x - 2), int(self.y - 3)),
            3
        )


# =====================================================
# PADDLE CLASS
# =====================================================

class Striker:

    def __init__(self):

        self.width = 110
        self.height = 22

        self.x = WIDTH // 2 - self.width // 2
        self.y = 438

        self.speed = 8

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, direction):

        self.x += direction * self.speed

        self.x = max(
            0,
            min(WIDTH - self.width, self.x)
        )

        self.rect.x = round(self.x)

    def display(self):

        shadow = self.rect.copy()
        shadow.y += 4

        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            shadow,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            PINK,
            self.rect,
            border_radius=12
        )

        pygame.draw.line(
            screen,
            LIGHT_PINK,
            (self.rect.x + 12, self.rect.y + 4),
            (self.rect.right - 12, self.rect.y + 4),
            3
        )

        draw_heart(
            screen,
            self.rect.centerx,
            self.rect.centery + 3,
            10,
            WHITE
        )

    def getRect(self):

        return self.rect


# =====================================================
# COLLISION DETECTION
# =====================================================

def check_block_collision(ball, block):

    ball_rect = ball.getRect()
    block_rect = block.getRect()

    if not ball_rect.colliderect(block_rect):
        return False

    # Determine collision using previous position
    previous_x = ball.x - ball.dx * ball.speed
    previous_y = ball.y - ball.dy * ball.speed

    previous_rect = pygame.Rect(
        round(previous_x - ball.radius),
        round(previous_y - ball.radius),
        ball.radius * 2,
        ball.radius * 2
    )

    # Hit from top
    if previous_rect.bottom <= block_rect.top + 2:

        ball.y = block_rect.top - ball.radius - 0.5
        ball.dy = -abs(ball.dy)

    # Hit from bottom
    elif previous_rect.top >= block_rect.bottom - 2:

        ball.y = block_rect.bottom + ball.radius + 0.5
        ball.dy = abs(ball.dy)

    # Hit from left
    elif previous_rect.right <= block_rect.left + 2:

        ball.x = block_rect.left - ball.radius - 0.5
        ball.dx = -abs(ball.dx)

    # Hit from right
    elif previous_rect.left >= block_rect.right - 2:

        ball.x = block_rect.right + ball.radius + 0.5
        ball.dx = abs(ball.dx)

    else:

        # Fallback: minimum penetration axis
        overlap_left = ball_rect.right - block_rect.left
        overlap_right = block_rect.right - ball_rect.left

        overlap_top = ball_rect.bottom - block_rect.top
        overlap_bottom = block_rect.bottom - ball_rect.top

        min_x = min(overlap_left, overlap_right)
        min_y = min(overlap_top, overlap_bottom)

        if min_x < min_y:

            ball.dx *= -1

        else:

            ball.dy *= -1

    return True


def check_paddle_collision(ball, paddle):

    ball_rect = ball.getRect()
    paddle_rect = paddle.getRect()

    if not ball_rect.colliderect(paddle_rect):
        return

    if ball.dy <= 0:
        return

    ball.y = paddle_rect.top - ball.radius - 1

    offset = (
        ball.x - paddle_rect.centerx
    ) / (paddle.width / 2)

    ball.dx = max(
        -1.2,
        min(1.2, offset * 1.2)
    )

    if abs(ball.dx) < 0.2:

        ball.dx = random.choice([-0.35, 0.35])

    ball.dy = -abs(ball.dy)


# =====================================================
# HUD
# =====================================================

def draw_hud(score, lives):

    # Lives capsule
    pygame.draw.rect(
        screen,
        BABY_PINK,
        (25, 18, 145, 43),
        border_radius=22
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (28, 21, 139, 37),
        2,
        border_radius=20
    )

    draw_heart(
        screen,
        53,
        39,
        13,
        PINK
    )

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        WHITE
    )

    screen.blit(lives_text, (75, 29))

    # Score capsule
    pygame.draw.rect(
        screen,
        BABY_PINK,
        (225, 18, 150, 43),
        border_radius=22
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (228, 21, 144, 37),
        2,
        border_radius=20
    )

    draw_star(
        screen,
        251,
        40,
        12,
        GOLD
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (275, 29))

    # Music decoration
    pygame.draw.circle(
        screen,
        PINK,
        (500, 40),
        19
    )

    music_text = font.render(
        "♪",
        True,
        WHITE
    )

    screen.blit(
        music_text,
        music_text.get_rect(center=(500, 40))
    )

    # Pause decoration
    pygame.draw.circle(
        screen,
        PINK,
        (550, 40),
        19
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (545, 31, 4, 17),
        border_radius=2
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (552, 31, 4, 17),
        border_radius=2
    )


# =====================================================
# GAME MESSAGE
# =====================================================

def draw_message(title, subtitle):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((55, 20, 55, 120))

    screen.blit(overlay, (0, 0))

    title_surface = large_font.render(
        title,
        True,
        WHITE
    )

    subtitle_surface = font.render(
        subtitle,
        True,
        LIGHT_PINK
    )

    screen.blit(
        title_surface,
        title_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 20)
        )
    )

    screen.blit(
        subtitle_surface,
        subtitle_surface.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 25)
        )
    )


# =====================================================
# MAIN GAME
# =====================================================

def main():

    running = True

    lives = 3
    score = 0

    striker = Striker()

    ball = Ball()
    ball.reset(striker)

    blocks = populateBlocks()

    game_state = "ready"

    while running:

        clock.tick(FPS)

        direction = 0

        # =============================================
        # EVENTS
        # =============================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    running = False

                elif event.key == pygame.K_SPACE:

                    if game_state == "ready":

                        ball.launch()
                        game_state = "playing"

                    elif game_state in ("win", "gameover"):

                        lives = 3
                        score = 0

                        striker = Striker()

                        ball = Ball()
                        ball.reset(striker)

                        blocks = populateBlocks()

                        game_state = "ready"

                elif event.key == pygame.K_p:

                    if game_state == "playing":

                        game_state = "pause"

                    elif game_state == "pause":

                        game_state = "playing"

        # =============================================
        # MOVEMENT
        # =============================================

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            direction = -1

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            direction = 1

        if game_state in ("playing", "ready"):

            striker.update(direction)

        # Ball follows paddle before launch
        if game_state == "ready":

            ball.x = striker.rect.centerx

            ball.y = striker.rect.top - ball.radius - 8

        # =============================================
        # GAME UPDATE
        # =============================================

        if game_state == "playing":

            # Save previous ball position
            previous_x = ball.x
            previous_y = ball.y

            # Move ball
            life_lost = ball.update()

            # Wall and bottom collision are handled in update
            if life_lost:

                lives -= 1

                if lives <= 0:

                    game_state = "gameover"

                else:

                    ball.reset(striker)

                    game_state = "ready"

            else:

                # Paddle collision
                check_paddle_collision(ball, striker)

                # Check only the first collided block
                for block in blocks:

                    if check_block_collision(ball, block):

                        block.hit()

                        if not block.alive:

                            blocks.remove(block)

                            score += 5

                        # One collision per frame
                        break

                # Win condition
                if len(blocks) == 0:

                    game_state = "win"

        # =============================================
        # DRAW
        # =============================================

        draw_background()

        # Individual Hello Kitty bricks
        for block in blocks:

            block.display()

        # Paddle
        striker.display()

        # Meteor ball
        ball.display()

        # HUD
        draw_hud(score, lives)

        # Game states
        if game_state == "ready":

            draw_message(
                "PINK BLOCK BREAKER",
                "PRESS SPACE TO START"
            )

        elif game_state == "pause":

            draw_message(
                "PAUSED",
                "PRESS P TO CONTINUE"
            )

        elif game_state == "win":

            draw_message(
                "YOU WIN!",
                "PRESS SPACE TO PLAY AGAIN"
            )

        elif game_state == "gameover":

            draw_message(
                "GAME OVER",
                "PRESS SPACE TO RESTART"
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# =====================================================
# RUN GAME
# =====================================================

if __name__ == "__main__":

    main()
