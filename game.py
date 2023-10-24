import pygame, os, random
import tkinter as tk
from tkinter import *
from tkinter import ttk


class Player:
    vel_x = 0
    vel_y = 0
    acc = 0.2

    def __init__(self, x, y, width, height):
        self.shoots = []
        self.x, self.y, self.width, self.height = x, y, width, height
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "player.png")), (width, height)
        )

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            shoot = Shoot(self)
            self.shoots.append(shoot)
        if self.y > 0:
            if keys[pygame.K_UP]:
                self.vel_y -= self.acc
        else:
            if not keys[pygame.K_DOWN]:
                self.y = 0
                self.vel_y = 0
        if self.y + self.height < HEIGHT:
            if keys[pygame.K_DOWN]:
                self.vel_y += self.acc
        else:
            if not keys[pygame.K_UP]:
                self.y = HEIGHT - self.height
                self.vel_y = 0
        if PLAYER_BACKFORTH:
            if self.x > 0:
                if keys[pygame.K_LEFT]:
                    self.vel_x -= self.acc
            else:
                if not keys[pygame.K_RIGHT]:
                    self.x = 0
                    self.vel_x = 0
            if self.x + self.width < WIDTH:
                if keys[pygame.K_RIGHT]:
                    self.vel_x += self.acc
            else:
                if not keys[pygame.K_LEFT]:
                    self.x = WIDTH - self.width
                    self.vel_x = 0

        self.vel_x = min(5, self.vel_x)
        self.vel_y = min(5, self.vel_y)
        self.vel_x = max(-5, self.vel_x)
        self.vel_y = max(-5, self.vel_y)

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, win):
        win.blit(self.image, (round(self.x), round(self.y)))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    

class Heart:
    def __init__(self):
        self.heart = 3
        self.x = 25
        self.y = 25
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "heart.png")), (25, 25)
        )

    def draw(self, win):
        for heart_num in range(self.heart):
            win.blit(self.image, (round(self.x) + heart_num * 30, round(self.y)))


class Shoot:
    WIDTH, HEIGHT = 5, 5
    VEL = 20

    def __init__(self, player):
        self.x, self.y = player.x + 80, player.y + 30
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "shoot.png")),
            (self.WIDTH, self.HEIGHT),
        )

    def move(self, player, bullets):
        self.x += self.VEL

        for bullet in bullets:
            if self.collide(bullet):
                bullets.remove(bullet)
                player.shoots.remove(self)
                return "crash"

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, bullet):
        bullet_mask = bullet.get_mask()
        mask = pygame.mask.from_surface(self.image)
        top_offset = (round(self.x - bullet.x), round(self.y - bullet.y))
        top_point = bullet_mask.overlap(mask, top_offset)

        if top_point:
            return True

        return False


class Bullet:
    WIDTH, HEIGHT = 80, 30
    VEL = 5

    def __init__(self, y):
        self.x, self.y = WIDTH + random.randint(0, 800), y
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "bullet.png")),
            (self.WIDTH, self.HEIGHT),
        )

    def move(self, player):
        self.x -= self.VEL

        if self.collide(player):
            return "crash"
        if self.x + self.WIDTH < 0:
            return "out"

        return False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, player):
        player_mask = player.get_mask()
        mask = pygame.mask.from_surface(self.image)
        top_offset = (round(self.x - player.x), round(self.y - player.y))
        top_point = player_mask.overlap(mask, top_offset)

        if top_point:
            return True

        return False

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Clouds:
    VEL = 2

    def __init__(self):
        self.y = 0
        self.x1 = 0
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "clouds_bg.png")), (WIDTH, HEIGHT)
        )
        self.width = self.image.get_width()
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))


def draw_window(win, hearts, player, shoots, clouds, bullets, score, max_score, playing):
    clouds.draw(win)
    player.draw(win)
    hearts.draw(win)
    for shoot in shoots:
        shoot.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    text1 = FONT.render(f"Max Score: {max_score}", 1, BLACK)
    text2 = FONT.render(f"Score: {score}", 1, BLACK)
    win.blit(text1, (WIDTH - text1.get_width() - 1, 5))
    win.blit(text2, (WIDTH - text2.get_width() - 5, 5 + text1.get_height() + 5))
    if not playing:
        text = BIG_FONT.render("Press SPACEBAR to play", 1, BLACK)
        win.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
        )


def create_bullets(n):
    bullets = []
    for _ in range(round(n)):
        bullets.append(Bullet(random.randint(0, HEIGHT - 15)))

    return bullets


def adjust_bullets(bullets, n):
    if len(bullets) > round(n):
        bullets.pop(0)
    elif len(bullets) < round(n):
        bullets.append(Bullet(random.randint(0, HEIGHT - 15)))

    return bullets


def end_menu(score):
    global WINDOW, username

    #Create an instance of Tkinter frame
    win = Tk()
    win.title("Game Over!")

    #Set the geometry of Tkinter frame
    win.geometry("550x150")

    def start_clicked():
        global FONT, BIG_FONT
        win.destroy()
        
        pygame.init()

        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (
        screen_width // 2 - WIDTH // 2,
        screen_height // 2 - HEIGHT // 2,
        )
        
        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dodger Plane")
        pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.png")))
        FONT = pygame.font.SysFont("comicsans", 30)
        BIG_FONT = pygame.font.SysFont("comicsans", 70)
        
        main(WINDOW, username)
        return
    
    # def score_clicked():
    #     return

    #Initialize a Label to display the User Input
    label=Label(win, text="Score : " + str(score), font=("Courier 18 bold"))
    label.pack(pady=20)

    # Add an empty label to create vertical spacing
    empty_label = Label(win, height=1)
    empty_label.pack()

    #Create a Button to validate Entry Widget
    button_start = ttk.Button(win, text="Start Again", width= 20, command=start_clicked)
    button_start.place(relx=0.5, rely=0.55, anchor="center")

    # button_score = ttk.Button(win, text="Score Board", width= 20, command=score_clicked)
    # button_score.place(relx=0.5, rely=0.65, anchor="center")

    win.mainloop()
    
    return

def move_bullets(hearts, player, shoots, bullets, score, n):
    rem = []
    for bullet in bullets:
        movement = bullet.move(player)
        if movement == "out":
            rem.append(bullet)
            score += 1
        if movement == "crash":
            hearts.heart -= 1
            bullets.remove(bullet)
            if hearts.heart == 0:
                pygame.quit()
                with open("scores.txt", "a") as f:
                    f.write(username + " " + str(score) + "\n")
                end_menu(score)
                return
    for shoot in shoots:
        movement = shoot.move(player, bullets)
        if movement == "crash":
            score += 10
    for bullet in rem:
        try:
            bullets.remove(bullet)
        except ValueError:
            pass

    while len(bullets) != round(n):
        bullets = adjust_bullets(bullets, n)

    return hearts, player, shoots, bullets, score, n


def move_objs(hearts, player, shoots, bullets, score, n, clouds):
    player.move()
    clouds.move()
    return move_bullets(hearts, player, shoots, bullets, score, n)


def main(win, username):
    clock = pygame.time.Clock()
    hearts = Heart()
    player = Player(random.randint(5, 35), random.randint(0, HEIGHT - 50), 100, 50)
    clouds = Clouds()
    shoots = player.shoots
    n = 5
    bullets = create_bullets(n)
    score = 0
    try:
        with open("max_score.txt", "r") as f:
            line = f.readline()
            max_score = int(line)
    except FileNotFoundError:
        max_score = 0
    run = True
    playing = False
    while run:
        clock.tick(FPS)
        draw_window(win, hearts, player, shoots, clouds, bullets, score, max_score, playing)
        n = min(30, n)
        if playing:
            n += 0.001
            try:
                hearts, player, shoots, bullets, score, n = move_objs(hearts, player, shoots, bullets, score, n, clouds)
            except:
                break
        if max_score < score:
            max_score = score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("max_score.txt", "w") as f:
                    f.write(str(max_score))
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = True if playing == False else False
        pygame.display.update()
    return
        

#Create an instance of Tkinter frame
win = Tk()
win.title("Welcome! ^^")

#Set the geometry of Tkinter frame
win.geometry("550x200")

clicked = False
username = ""

def close():
   global clicked, username
   clicked = True
   username = entry.get() 
   win.destroy()

#Initialize a Label to display the User Input
label=Label(win, text="What's your name? :)", font=("Courier 18 bold"))
label.pack(pady=20)

# Add an empty label to create vertical spacing
empty_label = Label(win, height=1)
empty_label.pack()

#Create an Entry widget to accept User Input
entry = Entry(win, width=40)
entry.focus_set()
entry.pack()

#Create a Button to validate Entry Widget
ttk.Button(win, text="Okay", width= 20, command=close).pack(pady=30)

win.mainloop()

WIDTH, HEIGHT = 1000, 700
FPS = 60

if clicked:
    pygame.init()

    screen_width = tk.Tk().winfo_screenwidth()
    screen_height = tk.Tk().winfo_screenheight()

    os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (
        screen_width // 2 - WIDTH // 2,
        screen_height // 2 - HEIGHT // 2,
    )
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodger Plane")
    pygame.display.set_icon(pygame.image.load(os.path.join("assets", "icon.png")))

    PLAYER_BACKFORTH = True

    FONT = pygame.font.SysFont("comicsans", 30)
    BIG_FONT = pygame.font.SysFont("comicsans", 70)


    BLACK = (0, 0, 0)
    main(WINDOW, username)
