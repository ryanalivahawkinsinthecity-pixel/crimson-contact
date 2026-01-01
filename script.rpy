# Crimson Contract - Complete Gothic BL VN
# Branching story, romance, humanity, skill tree, combat, cinematic effects

define p = Character("You", what_slow_cps=25)
define a = Character("Aurelian", what_slow_cps=25)

# ---------------- Variables ----------------
default username = ""
default humanity = 100
default romance = 0
default skills = []
default separated = False

# ---------------- Images ----------------
image bg cathedral = "images/cathedral.jpg"
image aurelian neutral = "images/aurelian_neutral.png"
image aurelian happy = "images/aurelian_happy.png"
image aurelian sad = "images/aurelian_sad.png"
image aurelian blink:
    "images/aurelian_neutral.png"
    pause 0.2
    "images/aurelian_blink.png"
    pause 0.1
    repeat
image player default = "images/player_default.png"
image blood_flash = Solid("#8B0000")
image fog_overlay = "images/fog.png"
image rain_overlay = "images/rain.png"

# ---------------- Transforms ----------------
transform shake:
    xoffset 0
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    repeat 5

transform blood_flash_effect:
    alpha 0.0
    linear 0.1 alpha 0.7
    linear 0.2 alpha 0.0

transform overlay_loop:
    linear 1.0 yoffset 0
    linear 1.0 yoffset -10
    repeat

# ---------------- Start ----------------
label start:
    play music "audio/menu.ogg" fadein 1.0
    scene bg cathedral with fade
    "Enter your name:"
    $ username = renpy.input("Name: ", length=12)
    $ username = username.strip()
    
    play music "audio/act1.ogg" fadein 1.0
    jump act1_1

# ---------------- ACT 1 ----------------
label act1_1:
    show aurelian neutral at center with fade
    a "So… they finally sent you."

    menu:
        "I’m a hunter.":
            $ romance -= 1
            jump act1_2
        "I’m an executioner.":
            $ romance += 1
            jump act1_2

label act1_2:
    show aurelian blink at center with dissolve
    a "Come closer. I want to remember you."
    menu:
        "Step closer.":
            $ romance += 2
            jump act2_1
        "Remain distant.":
            jump act2_1

# ---------------- ACT 2 ----------------
label act2_1:
    show aurelian neutral at center with fade
    a "You spare monsters too often."
    menu:
        "They deserve mercy.":
            $ humanity += 5
            $ romance += 1
            jump act2_2
        "Power matters more.":
            $ humanity -= 10
            $ romance -= 1
            jump act2_2

label act2_2:
    show aurelian sad at center with fade
    a "Don’t look at me like that."
    menu:
        "Drink. I trust you.":
            $ humanity -= 10
            $ romance += 3
            call skill_tree
            jump check_separation
        "I won’t become you.":
            $ romance -= 1
            jump check_separation

# ---------------- SEPARATION ----------------
label check_separation:
    if humanity <= 60 or romance <= 1:
        $ separated = True
        jump separation
    else:
        jump final

label separation:
    play music "audio/separation.ogg" fadein 1.0
    scene bg cathedral with fade
    show rain_overlay at overlay_loop
    show aurelian sad at center with dissolve
    a "If I stay, I will either stop you… or become you."
    a "I must go."
    
    menu:
        "Say nothing.":
            hide rain_overlay
            jump alone
        "Beg him to stay.":
            $ romance -= 1
            hide rain_overlay
            jump alone

label alone:
    "You grow stronger. Alone. Power answers faster now."
    jump reunion_check

# ---------------- REUNION ----------------
label reunion_check:
    if romance >= 4 and humanity >= 50:
        jump reunion
    else:
        jump final

label reunion:
    play music "audio/reunion.ogg" fadein 1.0
    scene bg cathedral with fade
    show aurelian happy at center with dissolve
    a "I told myself I wouldn’t come back."
    menu:
        "Don’t disappear again.":
            $ romance += 3
            jump final
        "Leave if you must.":
            jump final

# ---------------- FINAL ----------------
label final:
    play music "audio/ending.ogg" fadein 1.0

    if romance >= 5 and humanity < 50:
        show blood_flash onlayer master at blood_flash_effect
        "You are turned. You rule eternity together with Aurelian."
        hide blood_flash

    elif romance >= 4 and humanity >= 50:
        show rain_overlay at overlay_loop
        "You die human. Aurelian remembers you forever."
        hide rain_overlay

    elif romance < 4:
        show fog_overlay at overlay_loop
        "You vanish. Two shadows never meet again."
        hide fog_overlay

    elif separated:
        show rain_overlay at overlay_loop
        "You grow stronger. Alone. Power answers faster now."
        hide rain_overlay

    if "Blood Slash" in skills and "Veil Step" in skills and "Eternal Hunger" in skills:
        show blood_flash onlayer master at blood_flash_effect
        "With your skills mastered, your legend is eternal."
        hide blood_flash

    "THE END"
    return

# ---------------- SKILL TREE ----------------
label skill_tree:
    if humanity <= 60 and "Blood Slash" not in skills:
        menu:
            "Unlock Blood Slash?":
                "Yes":
                    $ skills.append("Blood Slash")
                    show blood_flash onlayer master at blood_flash_effect
                    pause 0.3
                    hide blood_flash
                "No":
                    pass
    if humanity <= 40 and "Veil Step" not in skills:
        menu:
            "Unlock Veil Step?":
                "Yes":
                    $ skills.append("Veil Step")
                "No":
                    pass
    if humanity <= 20 and "Eternal Hunger" not in skills:
        menu:
            "Unlock Eternal Hunger?":
                "Yes":
                    $ skills.append("Eternal Hunger")
                "No":
                    pass
    return

# ---------------- COMBAT ----------------
label combat(enemy="Vampire Spawn", enemy_hp=30):
    $ player_hp = 100
    while enemy_hp > 0 and player_hp > 0:
        "[enemy] HP: [enemy_hp] | Your HP: [player_hp]"
        menu:
            "Normal Attack":
                $ enemy_hp -= 10
                $ player_hp -= 8
                show blood_flash onlayer master at blood_flash_effect
                pause 0.3
                hide blood_flash
            "Blood Slash" if "Blood Slash" in skills:
                $ enemy_hp -= 25
                $ humanity -= 5
                $ player_hp -= 8
                show blood_flash onlayer master at blood_flash_effect
                pause 0.3
                hide blood_flash
            "Veil Step" if "Veil Step" in skills:
                $ enemy_hp -= 18
                $ romance -= 1
                $ player_hp -= 8
                show shake
        if player_hp <= 0:
            "You were defeated..."
            return
    "Enemy defeated!"
    return
