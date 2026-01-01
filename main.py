import pygame, sys, time

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 960, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crimson Contract")

FONT = pygame.font.SysFont("timesnewroman", 28)
SMALL = pygame.font.SysFont("timesnewroman", 22)
CLOCK = pygame.time.Clock()

BLACK = (10,10,10)
WHITE = (230,230,230)
CRIMSON = (140,0,0)

# ---------------- MUSIC & SFX ----------------
def play_music(track, vol=0.4):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(f"assets/music/{track}")
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play(-1)

def play_sfx(file, vol=0.5):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(vol)
    sound.play()

play_music("menu.mp3")

# ---------------- SPRITES ----------------
def load_sprite(path):
    return pygame.image.load(path).convert_alpha()

sprites = {
    "aurelian": {
        "neutral": load_sprite("assets/sprites/aurelian/neutral.png"),
        "happy": load_sprite("assets/sprites/aurelian/happy.png"),
        "sad": load_sprite("assets/sprites/aurelian/sad.png"),
        "angry": load_sprite("assets/sprites/aurelian/angry.png"),
    },
    "player": {
        "default": load_sprite("assets/sprites/player/default.png")
    }
}

def draw_character(character, expression, x=500, y=100):
    SCREEN.blit(sprites[character][expression], (x, y))

# ---------------- GAME STATE ----------------
state = "menu"
username = ""
humanity = 100
romance = 0
separated = False
skills = []
scene_id = "act1_1"
current_music = None

# ---------------- TYPEWRITER TEXT ----------------
def draw_text_typewriter(text, y, color=WHITE, speed=20):
    x = 60
    for i, char in enumerate(text):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        SCREEN.fill(BLACK, (x, y, WIDTH, 40))
        SCREEN.blit(SMALL.render(text[:i+1], True, color), (x, y))
        pygame.display.flip()
        pygame.time.delay(speed)

def draw_text(text, y, color=WHITE):
    lines = text.split("\n")
    for i, l in enumerate(lines):
        surf = SMALL.render(l, True, color)
        SCREEN.blit(surf, (60, y + i*28))

# ---------------- SKILL TREE ----------------
def update_skills():
    global skills
    available = []
    if humanity <= 60 and "Blood Slash" not in skills:
        available.append("Blood Slash")
    if humanity <= 40 and "Veil Step" not in skills:
        available.append("Veil Step")
    if humanity <= 20 and "Eternal Hunger" not in skills:
        available.append("Eternal Hunger")
    if available:
        choosing = True
        while choosing:
            SCREEN.fill(BLACK)
            draw_text("Choose a skill to unlock:", 200)
            for i, s in enumerate(available):
                draw_text(f"{i+1}. {s}", 240 + i*30)
            draw_text("Press corresponding number", 400)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    idx = event.key - pygame.K_1
                    if 0 <= idx < len(available):
                        skills.append(available[idx])
                        choosing = False

# ---------------- COMBAT ----------------
def combat(enemy_name="Vampire Spawn", enemy_hp=30):
    global humanity, romance
    player_hp = 100
    running_combat = True
    while running_combat:
        SCREEN.fill(BLACK)
        draw_text(f"Combat: {enemy_name}", 180, CRIMSON)
        draw_text(f"Enemy HP: {enemy_hp}", 220, CRIMSON)
        draw_text(f"Your HP: {player_hp}", 260, CRIMSON)
        draw_text("1. Normal Attack  2. Blood Slash  3. Veil Step", 320)
        draw_text("Press 1-3 to attack", 360)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                dmg = 10
                if event.key == pygame.K_2 and "Blood Slash" in skills:
                    dmg += 15
                    humanity -= 5
                    play_sfx("assets/sfx/blood_drink.wav")
                if event.key == pygame.K_3 and "Veil Step" in skills:
                    dmg += 8
                    romance -= 1
                enemy_hp -= dmg
                player_hp -= 8
                if player_hp <= 0:
                    draw_text("You were defeated...", 400, CRIMSON)
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    running_combat = False
                if enemy_hp <= 0:
                    draw_text(f"{enemy_name} defeated!", 400, CRIMSON)
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    running_combat = False
        pygame.display.flip()
        CLOCK.tick(60)

# ---------------- SCENES ----------------
SCENES = {
    "act1_1": {
        "music": "act1.mp3",
        "text": "Beneath the cathedral, chains whisper.\nAurelian waits for you.\n\nAurelian: “So… they finally sent you.”",
        "expression": "neutral",
        "choices": [
            ("I’m a hunter.", {"romance": -1}, "act1_2"),
            ("I’m an executioner.", {"romance": +1}, "act1_2")
        ]
    },
    "act1_2": {
        "text": "Aurelian studies your face.\n\n“Come closer. I want to remember you.”",
        "expression": "neutral",
        "choices": [
            ("Step closer.", {"romance": +2}, "act2_1"),
            ("Remain distant.", {}, "act2_1")
        ]
    },
    "act2_1": {
        "text": "Weeks pass. He walks beside you now.\n\nAurelian: “You spare monsters too often.”",
        "expression": "neutral",
        "choices": [
            ("They deserve mercy.", {"humanity": +5, "romance": +1}, "act2_2"),
            ("Power matters more.", {"humanity": -10, "romance": -1}, "act2_2")
        ]
    },
    "act2_2": {
        "text": "You are wounded. Blood spills.\n\nAurelian trembles.\n“Don’t look at me like that.”",
        "expression": "sad",
        "choices": [
            ("Drink. I trust you.", {"humanity": -10, "romance": +3}, "check_separation"),
            ("I won’t become you.", {"romance": -1}, "check_separation")
        ]
    },
    "check_separation": {"logic":"separation_check"},
    "separation": {
        "music":"separation.mp3",
        "text":"Rain falls.\n\nAurelian: “If I stay, I will either stop you… or become you.”\n\nHe turns away.",
        "expression":"sad",
        "choices":[
            ("Say nothing.", {}, "alone"),
            ("Beg him to stay.", {"romance": -1}, "alone")
        ]
    },
    "alone":{
        "text":"You grow stronger.\nAlone.\n\nPower answers faster now.",
        "choices":[("Continue.", {}, "reunion_check")]
    },
    "reunion_check":{"logic":"reunion_check"},
    "reunion":{
        "music":"reunion.mp3",
        "text":"Aurelian emerges from shadow.\n\n“I told myself I wouldn’t come back.”",
        "expression":"happy",
        "choices":[
            ("Don’t disappear again.", {"romance": +3}, "final"),
            ("Leave if you must.", {}, "final")
        ]
    },
    "final":{
        "music":"ending.mp3",
        "text":"The world holds its breath.\n\nThis is where your story ends.",
        "choices":[("Face your fate.", {}, "ending")]
    }
}

# ---------------- LOGIC HANDLERS ----------------
def separation_check():
    global separated, scene_id
    if humanity <= 60 or romance <= 1:
        separated = True
        scene_id = "separation"
    else:
        scene_id = "final"

def reunion_check():
    global scene_id
    if romance >= 4 and humanity >= 50:
        scene_id = "reunion"
    else:
        scene_id = "final"

# ---------------- STORY SCENE ----------------
def story_scene():
    SCREEN.fill(BLACK)
    update_skills()
    scene = SCENES[scene_id]
    if "expression" in scene:
        draw_character("aurelian", scene["expression"], x=500, y=100)
    draw_text_typewriter(scene["text"], 180)
    draw_text(f"Humanity: {humanity}   Romance: {romance}", 40, CRIMSON)
    if "choices" in scene:
        for i, (choice, _, _) in enumerate(scene["choices"]):
            draw_text(f"{i+1}. {choice}", 420 + i*30)

# ---------------- ENDING ----------------
def draw_ending():
    SCREEN.fill(BLACK)
    if romance >= 5 and humanity < 50:
        text = "You are turned.\nYou rule eternity together."
    elif romance >= 4:
        text = "You die human.\nAurelian remembers you forever."
    else:
        text = "You vanish.\nTwo shadows never meet again."
    draw_text_typewriter(text, 240, CRIMSON)
    draw_text("Press ESC to quit", 520)

# ---------------- MAIN LOOP ----------------
running = True
while running:
    CLOCK.tick(60)
    SCREEN.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key == pygame.K_RETURN and username:
                    state = "game"
                    scene_id = "act1_1"
                    play_music("act1.mp3")
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode.isalpha() and len(username)<12:
                    username += event.unicode

            elif state == "game":
                scene = SCENES[scene_id]
                if "logic" in scene:
                    if scene["logic"]=="separation_check":
                        separation_check()
                    elif scene["logic"]=="reunion_check":
                        reunion_check()
                elif "choices" in scene:
                    if event.key in [pygame.K_1, pygame.K_2]:
                        idx = event.key - pygame.K_1
                        if idx < len(scene["choices"]):
                            _, effects, next_scene = scene["choices"][idx]
                            humanity += effects.get("humanity",0)
                            romance += effects.get("romance",0)
                            scene_id = next_scene

            elif state == "ending":
                if event.key == pygame.K_ESCAPE:
                    running = False

    # DRAW
    if state == "menu":
        draw_text("CRIMSON CONTRACT", 200, CRIMSON)
        draw_text("Enter your name:", 280)
        draw_text(username, 320, CRIMSON)
        draw_text("Press ENTER", 380)

    elif state == "game":
        scene = SCENES[scene_id]
        if "music" in scene and scene["music"] != current_music:
            play_music(scene["music"])
            current_music = scene["music"]
        story_scene()
        if scene_id == "ending":
            state = "ending"

    elif state == "ending":
        draw_ending()

    pygame.display.flip()

pygame.quit()
sys.exit()
