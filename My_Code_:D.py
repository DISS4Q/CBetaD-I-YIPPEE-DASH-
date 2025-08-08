#pgzero

import random

WIDTH = 600
HEIGHT = 300
TITLE = "YIPPEE DASH!!!"
FPS = 30

# Actores
alien = Actor('yippee', (50, 240), size=(92, 92))
background = Actor("background")
main_menu_bg = Actor("main_menu")
box = Actor('nightmare', (550, 240), size=(92, 92))
bee = Actor('remorseless', (550, 170), size=(92, 92))
genue = Actor('genue', (550, 80), size=(92, 92))
wall = Actor('wall', (550, 160), size=(40, 120))
go = Actor("go")

# Variables globales
new_image = 'yippee'
game_over = False
score = 0
speed = 8
max_speed = 20
puede_saltar = True
en_aire = False
bajando = False
wall_visible = False
in_main_menu = True
show_controls_text = True  # Control para el texto que cambia con Shift derecho

enemigos = [box, bee, genue]
enemy = random.choice(enemigos)

def draw():
   

    if in_main_menu:
        main_menu_bg.draw()
        screen.draw.text(
            "YIPPEE DASH!!!",
            center=(WIDTH // 2, 30),
            fontsize=48,
            color="white"
        )
        # Texto que cambia al presionar Shift derecho
        if show_controls_text:
            screen.draw.text(
                "Press Shift to view controls",
                center=(WIDTH // 2, HEIGHT - 40),
                fontsize=28,
                color="white"
            )
        else:
            screen.draw.text(
                "↑ To Jump ↓ To Duck → To Go Over The Wall",
                center=(WIDTH // 2, HEIGHT - 40),
                fontsize=28,
                color="yellow"
            )
        screen.draw.text(
            "Press Enter to Start",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=32,
            color="white"
        )
    else:
        background.draw()
        alien.draw()
        if wall_visible:
            wall.draw()
        else:
            enemy.draw()
        screen.draw.text(str(score), (10, 10), fontsize=32, color="white")

        if game_over:
            go.draw()
            screen.draw.text(
                "Press Left Arrow to Return to Menu",
                center=(WIDTH // 2, 150),
                fontsize=36,
                color="white"
            )

def update(dt):
    global game_over, en_aire, bajando, new_image, score, speed, enemy, puede_saltar, wall_visible, in_main_menu

    if in_main_menu:
        return

    if game_over:
        return

    if wall_visible:
        if wall.x > -20:
            wall.x -= speed
        else:
            game_over = True
            wall_visible = False
    else:
        if enemy.x > -20:
            enemy.x -= speed
        else:
            score += 1
            if speed < max_speed:
                speed += 0.5
            enemy = random.choice(enemigos)
            enemy.x = WIDTH + 50

    check_spawn_wall()

    # SALTO y CAIDA
    if en_aire and (keyboard.down or keyboard.s):
        alien.y = 240
        alien.image = 'duck'
        new_image = 'duck'
        en_aire = False
        bajando = False
        puede_saltar = True

    elif en_aire:
        if bajando:
            if alien.y < 240:
                alien.y += 6
            else:
                alien.y = 240
                en_aire = False
                bajando = False
                alien.image = 'yippee'
                new_image = 'yippee'
                puede_saltar = True
        else:
            if alien.y > 100:
                alien.y -= 10
            else:
                alien.y = 100
                clock.schedule(iniciar_caida, 0.25)

    # AGACHARSE en suelo
    if not en_aire and (keyboard.down or keyboard.s):
        if new_image != 'duck':
            alien.image = 'duck'
            new_image = 'duck'
            alien.y = 250
    elif not en_aire and new_image == 'duck':
        if not (keyboard.down or keyboard.s):
            alien.image = 'yippee'
            new_image = 'yippee'
            alien.y = 240

    # Hitboxes
    if new_image == "duck":
        alien_hitbox = Rect((alien.left + 10, alien.top + 30), (alien.width - 20, alien.height - 50))
    else:
        alien_hitbox = Rect((alien.left + 10, alien.top + 10), (alien.width - 20, alien.height - 20))

    if wall_visible:
        wall_hitbox = Rect((wall.left + 5, wall.top + 5), (wall.width - 10, wall.height - 10))
        if alien_hitbox.colliderect(wall_hitbox):
            game_over = True
    else:
        enemy_hitbox = Rect((enemy.left + 10, enemy.top + 10), (enemy.width - 20, enemy.height - 20))
        if alien_hitbox.colliderect(enemy_hitbox):
            game_over = True

def iniciar_caida():
    global bajando
    bajando = True

def permitir_salto():
    global puede_saltar
    puede_saltar = True

def on_key_down(key):
    global puede_saltar, en_aire, bajando, new_image, wall_visible, score, enemy, game_over, in_main_menu, show_controls_text

    if in_main_menu:
        if key == keys.RETURN:
            in_main_menu = False
            reiniciar()
        elif key == keys.RSHIFT:
            show_controls_text = not show_controls_text
        return

    if game_over:
        if key == keys.LEFT:
            in_main_menu = True
            game_over = False
        return

    # Saltar con espacio, flecha arriba o W
    if key in (keys.SPACE, keys.UP, keys.W) and puede_saltar and not en_aire and not game_over:
        puede_saltar = False
        en_aire = True
        bajando = False
        alien.image = 'alien_jump'
        new_image = 'alien_jump'

    # Agacharse con flecha abajo o S
    if key in (keys.DOWN, keys.S):
        if not en_aire and new_image != 'duck':
            alien.image = 'duck'
            new_image = 'duck'
            alien.y = 250

    # Vencer la pared solo con flecha derecha
    if key == keys.RIGHT:
        if wall_visible:
            wall_visible = False
            score += 1
            enemy = random.choice(enemigos)
            enemy.x = WIDTH + 50
            if speed < max_speed:
                speed += 0.5

def reiniciar():
    global game_over, alien, speed, score, enemy, new_image, en_aire, bajando, puede_saltar, wall_visible
    game_over = False
    alien.pos = (50, 240)
    alien.image = 'yippee'
    new_image = 'yippee'
    speed = 8
    score = 0
    en_aire = False
    bajando = False
    puede_saltar = True
    wall_visible = False
    for e in enemigos:
        e.x = 600
    enemy = random.choice(enemigos)

def check_spawn_wall():
    global wall_visible
    if not wall_visible and score > 0 and score % 5 == 0:
        wall_visible = True
        wall.x = WIDTH + 50
