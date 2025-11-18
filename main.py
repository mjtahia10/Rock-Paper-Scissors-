import pygame
import random
import os
import json
pygame.init()

WIDTH , HEIGHT = 1200, 710
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

BG_TOP = (245, 245, 255)
BG_BOTTOM = (210, 220, 255)
HEADER_COLOR = (30, 40 , 80)
WHITE = (255, 255, 255)
TEXT = (40, 40, 40)
GREEN = (60, 200, 90)
RED = (220, 70, 70)
BLUE = (60, 120, 230)
GRAY = (180, 180, 200)
BLUEVIOLET = (138, 43, 226)

TITLE_FONT = pygame.fon.SysFont("arialblack", 48)
LABEL_FONT = pygame.fon.SysFont("arial", 28)
SCORE_FONT = pygame.fon.SysFont("arial",32 , bold=True)
RESULT_FONT = pygame.fon.SysFont("arialblack", 32)

PLAYER_IMAGES = {
    "rock": pygame.image.load("rock.png"),
    "paper": pygame.image.load("paper.png"),
    "scissors": pygame.image.load("scissors.png")
    }
PC_IMAGES = {
    "rock": pygame.image.load("pc_rock.png"),
    "paper": pygame.image.load("pc_paper.png"),
    "scissors": pygame.image.load("pc_scissors.png")
    }

for k in PLAYER_IMAGES:
    PLAYER_IMAGES[k] = pygame.transform.scale(PLAYER_IMAGES[k], (230,230))
for k in PC_IMAGES:
    PC_IMAGES[k] = pygame.transform.scale(PC_IMAGES[k], (230,230))
    
class Button:
    def __init__(self, x, y, text, colour, hover_color, width=190, height=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.hover_color = hover_color
    def draw(self, screen, mouse_pos):
        clr = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen,color, self.rect, border_radius=12)
        text_surface = LABEL_FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
buttons = [
    Button(200, 550, "Rock", BLUE, (180, 150, 255)),
    Button(500, 550, "Paper", GREEN, (120, 220, 120)),
    Button(800, 550, "Scissors", RED, (255, 100, 100)),
    Button(WIDTH - 180, 20, "Reset", BLUEVIOLET, (150, 150, 180), 140, 50)
]

player_score = 0
pc_score = 0
high_score = 0
round_winner = " "
player_choice = " "
pc_choice = ""
training_path = "training_data.json"
default_training = {
    "total_games": 0,
    "player_move_count": { "rock": 0, "paper": 0, "scissors": 0},
    "player_transition": {
        "rock": { "rock": 0, "paper": 0, "scissors": 0},
        "paper": { "rock": 0, "paper": 0, "scissors": 0},
        "scissors": { "rock": 0, "paper": 0, "scissors": 0},
    },
    "last_player_move": None,
    "recent_player_moves": []
}
if os.path.exists(training_path):
    try:
        with open(training_path, "r") as f:
            training = json.load(f)
    except:
        training = default_training.copy()

training.setdefault("recent_player_moves", [])
training.setdefault("last_player_move", None)


if os.path.exists("highscore.txt"):
    try:
        with open("highscore.txt", "r") as f:
            training = int(f.read().strip())
    except:
        high_score = 0
        
def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))
        
def save_training():
    with open(training_path, "w") as f:
        json.dump(training, f)
        
def get_winner(player, pc):
    if player == pc:
        return "Draw"
    elif (player=="rock" and pc=="scissors") or (player=="paper" and pc=="rock") or (player=="scissors" and pc=="paper"):
        return "Player"
    else:
        return "Computer"
def update_training_after_round(player_move):
    training.setdefault("recent_player_moves", [])
    training.setdefault("last_player_move", None)
    training["total_games"] += 1
    training[player_move_count][player_move] += 1
    last = training.get("last_player_move")
    if last:
        training["player_transition"][last][player_move] += 1
    training["last_player_move"] = player_move
    training["recent_player_moves"].append(player_move)
    if len(training["recent_player_moves"]) > 20:
        training["recent_player_moves"].pop(0)
    save_training()
    